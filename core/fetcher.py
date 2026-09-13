"""
OmniProxy Harvester - Concurrent Multi-Feed Proxy Fetcher
Downloads and parses free public proxy feeds across HTTP, SOCKS4, and SOCKS5.
"""
import os
import re
import sys
import json
import asyncio
from typing import List, Dict, Set, Optional

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import httpx

# Regex to accurately capture IPv4:Port with optional protocol prefixes
PROXY_REGEX = re.compile(
    r"(?:(?P<proto>https?|socks4|socks5)://)?"
    r"(?P<ip>(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})"
    r":(?P<port>\d{2,5})",
    re.IGNORECASE
)

def load_sources_config(config_path: Optional[str] = None) -> Dict[str, List[str]]:
    """Load sources from json configuration file."""
    if not config_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, "config", "sources.json")
        
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"http": [], "socks4": [], "socks5": []}

async def fetch_single_source(client: httpx.AsyncClient, url: str, protocol: str) -> List[Dict[str, str]]:
    """Fetch and extract proxies from a single endpoint."""
    proxies = []
    try:
        resp = await client.get(url, timeout=12.0)
        if resp.status_code == 200:
            content = resp.text
            for match in PROXY_REGEX.finditer(content):
                ip = match.group("ip")
                port = match.group("port")
                if 1 <= int(port) <= 65535:
                    proxies.append({
                        "ip": ip,
                        "port": int(port),
                        "proxy": f"{ip}:{port}",
                        "protocol": protocol
                    })
    except Exception:
        pass
    return proxies

async def fetch_all_proxies(
    protocols: Optional[List[str]] = None, 
    country_filter: Optional[str] = None,
    config_path: Optional[str] = None,
    verbose: bool = True
) -> List[Dict[str, str]]:
    """
    Asynchronously scrape all endpoints across requested protocols.
    Deduplicates candidates and returns a unified list.
    """
    sources = load_sources_config(config_path)
    if not protocols or "all" in protocols:
        target_protocols = list(sources.keys())
    else:
        target_protocols = [p.lower() for p in protocols if p.lower() in sources]

    tasks = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    async with httpx.AsyncClient(headers=headers, verify=False, follow_redirects=True) as client:
        for proto in target_protocols:
            urls = sources.get(proto, [])
            for url in urls:
                target_url = url
                if country_filter and "proxyscrape.com" in target_url and "country=all" in target_url:
                    target_url = target_url.replace("country=all", f"country={country_filter.upper()}")
                tasks.append(fetch_single_source(client, target_url, proto))

        if verbose:
            c_info = f" (Country: {country_filter.upper()})" if country_filter else ""
            print(f"🌐 Fetching raw proxies from {len(tasks)} verified source feeds{c_info}...")

        results = await asyncio.gather(*tasks)

    # Deduplicate while preserving earliest protocol mapping
    seen_proxies: Set[str] = set()
    unique_candidates: List[Dict[str, str]] = []

    for batch in results:
        for item in batch:
            key = f"{item['protocol']}://{item['proxy']}"
            if key not in seen_proxies:
                seen_proxies.add(key)
                unique_candidates.append(item)

    if verbose:
        print(f"📦 Total unique candidates harvested: {len(unique_candidates):,} proxies")
        for proto in target_protocols:
            cnt = sum(1 for p in unique_candidates if p['protocol'] == proto)
            print(f"  • {proto.upper()}: {cnt:,} candidates")

    return unique_candidates

def fetch_proxies_sync(
    protocols: Optional[List[str]] = None, 
    country_filter: Optional[str] = None,
    config_path: Optional[str] = None
) -> List[Dict[str, str]]:
    """Synchronous convenience wrapper around fetch_all_proxies."""
    return asyncio.run(fetch_all_proxies(protocols=protocols, country_filter=country_filter, config_path=config_path))

