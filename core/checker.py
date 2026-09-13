"""
OmniProxy Harvester - High-Speed Multi-Protocol Proxy Checker
Tests connectivity, measures real-time latency, detects anonymity levels,
and enriches live proxies with GeoIP & ISP data.
Supports curl_cffi, requests, and zero-dependency urllib fallback.
"""
import sys
import time
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional
import concurrent.futures

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Optional curl_cffi for native libcurl SOCKS4/SOCKS5 performance
try:
    from curl_cffi import requests as curl_requests
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

DEFAULT_TEST_URL = "https://api.ipify.org?format=json"
_CACHED_HOST_IP: Optional[str] = None

def get_host_ip() -> str:
    """Retrieve host machine's external IP to detect transparent proxy leaks."""
    global _CACHED_HOST_IP
    if _CACHED_HOST_IP is not None:
        return _CACHED_HOST_IP

    endpoints = [
        "https://api.ipify.org?format=json",
        "https://icanhazip.com",
        "https://ifconfig.me/ip"
    ]
    for url in endpoints:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                raw = resp.read().decode("utf-8").strip()
                if raw.startswith("{"):
                    _CACHED_HOST_IP = json.loads(raw).get("ip", "").strip()
                else:
                    _CACHED_HOST_IP = raw.strip()
                if _CACHED_HOST_IP:
                    return _CACHED_HOST_IP
        except Exception:
            continue
    _CACHED_HOST_IP = ""
    return _CACHED_HOST_IP

def classify_anonymity(headers_obj: Any, egress_ip: str, host_ip: str) -> str:
    """
    Classify proxy anonymity level:
    - Transparent: Leaks real client IP
    - Anonymous: Hides real client IP, but indicates proxy usage via headers
    - Elite: Completely hides client IP and proxy presence
    """
    if host_ip and egress_ip and egress_ip == host_ip:
        return "Transparent"

    proxy_indicators = {
        "via", "x-forwarded-for", "forwarded", "x-real-ip", 
        "proxy-connection", "x-proxy-id", "x-cache"
    }

    found_proxy_header = False
    items = []
    if hasattr(headers_obj, "items"):
        items = headers_obj.items()
    elif isinstance(headers_obj, dict):
        items = headers_obj.items()

    for k, v in items:
        k_low = str(k).lower()
        v_str = str(v)
        if host_ip and host_ip in v_str:
            return "Transparent"
        if k_low in proxy_indicators:
            found_proxy_header = True

    if found_proxy_header:
        return "Anonymous"
    return "Elite"

def test_single_proxy(
    proxy_info: Dict[str, Any], 
    timeout: float = 3.0, 
    test_url: str = DEFAULT_TEST_URL,
    host_ip: str = ""
) -> Optional[Dict[str, Any]]:
    """
    Test a single proxy candidate across its designated protocol.
    Returns enriched dict if alive and valid, None otherwise.
    """
    proxy_str = proxy_info["proxy"]
    proto = proxy_info.get("protocol", "http").lower()
    url_proxy = f"{proto}://{proxy_str}"
    proxies = {"http": url_proxy, "https": url_proxy}
    
    t0 = time.perf_counter()
    try:
        if HAS_CURL_CFFI:
            resp = curl_requests.get(test_url, proxies=proxies, timeout=timeout)
            status_code = resp.status_code
            if 200 <= status_code < 400:
                elapsed = round(time.perf_counter() - t0, 3)
                public_ip = proxy_info.get("ip", proxy_str.split(":")[0])
                try:
                    data = resp.json()
                    public_ip = data.get("ip", public_ip)
                except Exception:
                    pass
                
                anon = classify_anonymity(resp.headers, public_ip, host_ip)
                return {
                    "ip": proxy_info.get("ip", proxy_str.split(":")[0]),
                    "port": proxy_info.get("port", int(proxy_str.split(":")[1])),
                    "proxy": proxy_str,
                    "protocol": proto,
                    "latency_sec": elapsed,
                    "latency_ms": int(elapsed * 1000),
                    "egress_ip": public_ip,
                    "anonymity": anon,
                    "country": "Unknown",
                    "country_code": "??",
                    "city": "-",
                    "isp": "-"
                }
        elif HAS_REQUESTS:
            resp = requests.get(test_url, proxies=proxies, timeout=timeout)
            status_code = resp.status_code
            if 200 <= status_code < 400:
                elapsed = round(time.perf_counter() - t0, 3)
                public_ip = proxy_info.get("ip", proxy_str.split(":")[0])
                try:
                    data = resp.json()
                    public_ip = data.get("ip", public_ip)
                except Exception:
                    pass
                
                anon = classify_anonymity(resp.headers, public_ip, host_ip)
                return {
                    "ip": proxy_info.get("ip", proxy_str.split(":")[0]),
                    "port": proxy_info.get("port", int(proxy_str.split(":")[1])),
                    "proxy": proxy_str,
                    "protocol": proto,
                    "latency_sec": elapsed,
                    "latency_ms": int(elapsed * 1000),
                    "egress_ip": public_ip,
                    "anonymity": anon,
                    "country": "Unknown",
                    "country_code": "??",
                    "city": "-",
                    "isp": "-"
                }
        else:
            # Fallback to standard library urllib
            proxy_handler = urllib.request.ProxyHandler({'http': url_proxy, 'https': url_proxy})
            opener = urllib.request.build_opener(proxy_handler)
            req = urllib.request.Request(test_url, headers={"User-Agent": "Mozilla/5.0"})
            with opener.open(req, timeout=timeout) as resp:
                status_code = resp.status
                if 200 <= status_code < 400:
                    elapsed = round(time.perf_counter() - t0, 3)
                    public_ip = proxy_info.get("ip", proxy_str.split(":")[0])
                    try:
                        data = json.loads(resp.read().decode("utf-8"))
                        public_ip = data.get("ip", public_ip)
                    except Exception:
                        pass
                    
                    anon = classify_anonymity(resp.headers, public_ip, host_ip)
                    return {
                        "ip": proxy_info.get("ip", proxy_str.split(":")[0]),
                        "port": proxy_info.get("port", int(proxy_str.split(":")[1])),
                        "proxy": proxy_str,
                        "protocol": proto,
                        "latency_sec": elapsed,
                        "latency_ms": int(elapsed * 1000),
                        "egress_ip": public_ip,
                        "anonymity": anon,
                        "country": "Unknown",
                        "country_code": "??",
                        "city": "-",
                        "isp": "-"
                    }
    except Exception:
        pass
    return None

def batch_enrich_geoip(live_proxies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Batch lookup GeoIP metadata in chunks of 100 via ip-api.com.
    """
    if not live_proxies:
        return []
    
    ip_map = {p["ip"]: p for p in live_proxies}
    ips_to_query = list(ip_map.keys())
    
    chunk_size = 100
    for i in range(0, len(ips_to_query), chunk_size):
        chunk = ips_to_query[i:i + chunk_size]
        try:
            if HAS_REQUESTS:
                r = requests.post("http://ip-api.com/batch", json=chunk, timeout=6.0)
                if r.status_code == 200:
                    data = r.json()
                    for item in data:
                        q_ip = item.get("query")
                        if q_ip in ip_map and item.get("status") == "success":
                            ip_map[q_ip]["country"] = item.get("country", "Unknown")
                            ip_map[q_ip]["country_code"] = item.get("countryCode", "??")
                            ip_map[q_ip]["city"] = item.get("city", "-")
                            ip_map[q_ip]["isp"] = item.get("isp", "-")
            else:
                req_data = json.dumps(chunk).encode("utf-8")
                req = urllib.request.Request(
                    "http://ip-api.com/batch",
                    data=req_data,
                    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=6.0) as r:
                    if r.status == 200:
                        data = json.loads(r.read().decode("utf-8"))
                        for item in data:
                            q_ip = item.get("query")
                            if q_ip in ip_map and item.get("status") == "success":
                                ip_map[q_ip]["country"] = item.get("country", "Unknown")
                                ip_map[q_ip]["country_code"] = item.get("countryCode", "??")
                                ip_map[q_ip]["city"] = item.get("city", "-")
                                ip_map[q_ip]["isp"] = item.get("isp", "-")
        except Exception:
            pass
            
    return live_proxies

def check_proxies_pool(
    candidates: List[Dict[str, Any]],
    max_check: int = 300,
    target_alive: int = 20,
    timeout: float = 3.0,
    max_workers: int = 60,
    country_filter: Optional[str] = None,
    anonymity_filter: Optional[str] = None,
    test_url: str = DEFAULT_TEST_URL,
    on_live_callback = None
) -> List[Dict[str, Any]]:
    """
    Concurrently check candidate proxies with early stop when target_alive is reached.
    Supports country and anonymity filtering, plus custom target URLs.
    Sorts verified proxies by lowest latency.
    """
    to_test = candidates[:max_check]
    alive_list: List[Dict[str, Any]] = []
    host_ip = get_host_ip()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {
            executor.submit(test_single_proxy, p, timeout, test_url, host_ip): p 
            for p in to_test
        }
        
        for future in concurrent.futures.as_completed(future_to_proxy):
            res = future.result()
            if res:
                # Anonymity filter check
                if anonymity_filter and anonymity_filter.lower() != "all":
                    if res.get("anonymity", "").lower() != anonymity_filter.lower():
                        continue

                # Country filter check
                if country_filter:
                    c_upper = country_filter.upper()
                    try:
                        url_geo = f"http://ip-api.com/json/{res['ip']}?fields=country,countryCode,city,isp,status"
                        if HAS_REQUESTS:
                            qr = requests.get(url_geo, timeout=2.5)
                            cd = qr.json() if qr.status_code == 200 else {}
                        else:
                            with urllib.request.urlopen(url_geo, timeout=2.5) as qr:
                                cd = json.loads(qr.read().decode("utf-8")) if qr.status == 200 else {}
                                
                        if cd.get("status") == "success":
                            res["country"] = cd.get("country", "Unknown")
                            res["country_code"] = cd.get("countryCode", "??")
                            res["city"] = cd.get("city", "-")
                            res["isp"] = cd.get("isp", "-")
                    except Exception:
                        pass

                    if res.get("country_code") != c_upper and res.get("country", "").upper() != c_upper:
                        continue

                alive_list.append(res)
                if on_live_callback:
                    on_live_callback(res, len(alive_list), target_alive)
                if len(alive_list) >= target_alive:
                    # Cancel remaining pending checks
                    for f in future_to_proxy:
                        f.cancel()
                    break

    # Enrich with GeoIP for general runs
    if alive_list and not country_filter:
        batch_enrich_geoip(alive_list)

    # Sort by lowest latency
    alive_list.sort(key=lambda x: x["latency_ms"])
    return alive_list
