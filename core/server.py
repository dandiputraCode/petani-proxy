"""
OmniProxy Harvester - Local Rotating Gateway & REST API Server
Provides a local forward-proxy endpoint (HTTP/HTTPS CONNECT) that automatically rotates
requests across verified alive proxies, plus a lightweight REST API.
Zero external dependencies (uses standard library socket, http.server, threading).
"""
import os
import sys
import json
import time
import socket
import select
import random
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import List, Dict, Any, Optional

class ProxyPoolManager:
    """Manages the in-memory pool of verified proxies with round-robin rotation."""
    def __init__(self, initial_proxies: Optional[List[Dict[str, Any]]] = None):
        self.lock = threading.Lock()
        self.proxies: List[Dict[str, Any]] = initial_proxies or []
        self.index = 0
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = time.time()

    def update_pool(self, new_proxies: List[Dict[str, Any]]):
        with self.lock:
            self.proxies = new_proxies
            self.index = 0

    def get_all(self) -> List[Dict[str, Any]]:
        with self.lock:
            return list(self.proxies)

    def get_random(self) -> Optional[Dict[str, Any]]:
        with self.lock:
            if not self.proxies:
                return None
            return random.choice(self.proxies)

    def get_next(self) -> Optional[Dict[str, Any]]:
        """Round-robin proxy selection."""
        with self.lock:
            if not self.proxies:
                return None
            proxy = self.proxies[self.index % len(self.proxies)]
            self.index += 1
            self.total_requests += 1
            return proxy

    def mark_result(self, success: bool):
        with self.lock:
            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1

    def get_stats(self) -> Dict[str, Any]:
        with self.lock:
            uptime = round(time.time() - self.start_time, 1)
            return {
                "uptime_seconds": uptime,
                "pool_size": len(self.proxies),
                "total_routed_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "current_index": self.index
            }


class RotatingProxyRequestHandler(BaseHTTPRequestHandler):
    """
    Handles both REST API endpoints and HTTP/HTTPS forward proxy requests.
    """
    pool_manager: ProxyPoolManager = None

    def log_message(self, format, *args):
        # Suppress noisy standard HTTP access logs
        pass

    # --- REST API Endpoints ---
    def do_GET(self):
        # Check if this is an API call
        path = self.path
        if path.startswith("/api/") or path == "/api" or path == "/":
            self.handle_api_request(path)
            return

        # Otherwise, treat as standard HTTP forward proxy request
        self.handle_http_forward()

    def handle_api_request(self, path: str):
        if path in ("/api/random", "/api/random/"):
            p = self.pool_manager.get_random()
            if p:
                payload = {
                    "status": "success",
                    "proxy": p.get("proxy"),
                    "protocol": p.get("protocol", "http"),
                    "url": f"{p.get('protocol', 'http')}://{p['proxy']}",
                    "country": p.get("country", "Unknown"),
                    "country_code": p.get("country_code", "??"),
                    "anonymity": p.get("anonymity", "Elite"),
                    "latency_ms": p.get("latency_ms", 0)
                }
            else:
                payload = {"status": "error", "message": "Proxy pool is empty"}
            self.send_json_response(payload)

        elif path in ("/api/all", "/api/all/"):
            proxies = self.pool_manager.get_all()
            self.send_json_response({
                "status": "success",
                "count": len(proxies),
                "proxies": proxies
            })

        elif path in ("/api/status", "/api/status/", "/", "/api"):
            stats = self.pool_manager.get_stats()
            self.send_json_response({
                "service": "OmniProxy Harvester Gateway & REST API",
                "version": "2.0.0",
                "maintainer": "@itzluthfi (github.com/itzluthfi)",
                "stats": stats,
                "endpoints": {
                    "random": "/api/random",
                    "all": "/api/all",
                    "status": "/api/status"
                },
                "forward_proxy_usage": "Configure HTTP/HTTPS proxy to http://127.0.0.1:8888"
            })
        else:
            self.send_error(404, "API endpoint not found")

    def send_json_response(self, data: dict, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    # --- HTTPS CONNECT Tunneling ---
    def do_CONNECT(self):
        """
        Handle HTTPS CONNECT method to create a TCP tunnel to the target host.
        """
        target_host, target_port = self.path.split(":")
        target_port = int(target_port)

        upstream_proxy = self.pool_manager.get_next()
        if not upstream_proxy:
            self.send_error(503, "No alive proxies available in pool")
            return

        u_ip = upstream_proxy["ip"]
        u_port = int(upstream_proxy["port"])

        try:
            # Connect to upstream proxy
            upstream_sock = socket.create_connection((u_ip, u_port), timeout=5.0)

            # Send CONNECT command to upstream proxy
            connect_req = f"CONNECT {target_host}:{target_port} HTTP/1.1\r\nHost: {target_host}:{target_port}\r\n\r\n"
            upstream_sock.sendall(connect_req.encode("utf-8"))

            # Read upstream response
            upstream_resp = upstream_sock.recv(4096).decode("utf-8", errors="ignore")
            if "200" not in upstream_resp:
                upstream_sock.close()
                self.pool_manager.mark_result(False)
                self.send_error(502, "Bad Gateway from upstream proxy")
                return

            # Tell client tunnel is established
            self.send_response(200, "Connection Established")
            self.end_headers()

            # Pipe bi-directional data between client and upstream
            self.pipe_sockets(self.connection, upstream_sock)
            self.pool_manager.mark_result(True)

        except Exception:
            self.pool_manager.mark_result(False)
            try:
                self.send_error(504, "Gateway Timeout")
            except Exception:
                pass

    def handle_http_forward(self):
        """
        Forward standard HTTP requests through upstream proxy.
        """
        upstream_proxy = self.pool_manager.get_next()
        if not upstream_proxy:
            self.send_error(503, "No alive proxies available in pool")
            return

        u_ip = upstream_proxy["ip"]
        u_port = int(upstream_proxy["port"])

        try:
            upstream_sock = socket.create_connection((u_ip, u_port), timeout=5.0)

            # Reconstruct HTTP request line and headers
            req_line = f"{self.command} {self.path} {self.request_version}\r\n"
            headers_str = "".join([f"{k}: {v}\r\n" for k, v in self.headers.items()])
            full_req = f"{req_line}{headers_str}\r\n".encode("utf-8")

            # Forward body if present
            content_len = int(self.headers.get("Content-Length", 0))
            if content_len > 0:
                body = self.rfile.read(content_len)
                full_req += body

            upstream_sock.sendall(full_req)

            # Pipe response back to client
            self.pipe_sockets(self.connection, upstream_sock)
            self.pool_manager.mark_result(True)

        except Exception:
            self.pool_manager.mark_result(False)
            try:
                self.send_error(502, "Bad Gateway")
            except Exception:
                pass

    def pipe_sockets(self, sock1: socket.socket, sock2: socket.socket, buffer_size: int = 8192, timeout: float = 30.0):
        """Pipes data bidirectionally between two sockets until closed."""
        sockets = [sock1, sock2]
        while True:
            r_socks, _, _ = select.select(sockets, [], [], timeout)
            if not r_socks:
                break
            for s in r_socks:
                data = s.recv(buffer_size)
                if not data:
                    return
                other = sock2 if s is sock1 else sock1
                other.sendall(data)


def start_proxy_server(
    initial_proxies: List[Dict[str, Any]], 
    host: str = "127.0.0.1", 
    port: int = 8888, 
    background: bool = False
) -> tuple[HTTPServer, ProxyPoolManager]:
    """
    Launch the Rotating Proxy Gateway and REST API server.
    """
    pool_mgr = ProxyPoolManager(initial_proxies)

    class CustomHandler(RotatingProxyRequestHandler):
        pool_manager = pool_mgr

    server = HTTPServer((host, port), CustomHandler)

    if background:
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
    else:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()

    return server, pool_mgr
