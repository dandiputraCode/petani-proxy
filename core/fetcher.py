"""
OmniProxy Harvester - Concurrent Multi-Feed Proxy Fetcher
Downloads and parses free public proxy feeds across HTTP, SOCKS4, and SOCKS5.
Supports httpx (async) with automatic fallback to urllib.request.
"""
import os
import re
import sys
import json
import asyncio
import urllib.request
import urllib.error
import concurrent.futures
from typing import List, Dict, Set, Optional

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

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

def _parse_proxies_from_text(content: str, protocol: str) -> List[Dict[str, str]]:
    proxies = []
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
    return proxies

async def fetch_single_source_async(client, url: str, protocol: str) -> List[Dict[str, str]]:
    """Fetch using httpx AsyncClient."""
    try:
        resp = await client.get(url, timeout=12.0)
        if resp.status_code == 200:
            return _parse_proxies_from_text(resp.text, protocol)
    except Exception:
        pass
    return []

def fetch_single_source_urllib(url: str, protocol: str) -> List[Dict[str, str]]:
    """Fallback fetch using standard urllib."""
    try:
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            text = resp.read().decode("utf-8", errors="ignore")
            return _parse_proxies_from_text(text, protocol)
    except Exception:
        pass
    return []

async def fetch_all_proxies_httpx(target_urls: List[tuple], verbose: bool, country_info: str) -> List[List[Dict[str, str]]]:
    tasks = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    async with httpx.AsyncClient(headers=headers, verify=False, follow_redirects=True) as client:
        for url, proto in target_urls:
            tasks.append(fetch_single_source_async(client, url, proto))
        if verbose:
            print(f"🌐 Fetching raw proxies from {len(tasks)} verified source feeds{country_info}...")
        return await asyncio.gather(*tasks)

def fetch_all_proxies_threaded(target_urls: List[tuple], verbose: bool, country_info: str) -> List[List[Dict[str, str]]]:
    if verbose:
        print(f"🌐 Fetching raw proxies from {len(target_urls)} verified source feeds{country_info} (urllib engine)...")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_url = {executor.submit(fetch_single_source_urllib, u, p): u for u, p in target_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                results.append(future.result())
            except Exception:
                pass
    return results

def fetch_proxies_sync(
    protocols: Optional[List[str]] = None, 
    country_filter: Optional[str] = None,
    config_path: Optional[str] = None,
    verbose: bool = True
) -> List[Dict[str, str]]:
    """
    Scrape all endpoints across requested protocols.
    Uses httpx async if available, else falls back to urllib threading.
    """
    sources = load_sources_config(config_path)
    if not protocols or "all" in protocols:
        target_protocols = list(sources.keys())
    else:
        target_protocols = [p.lower() for p in protocols if p.lower() in sources]

    target_urls = []
    for proto in target_protocols:
        urls = sources.get(proto, [])
        for url in urls:
            target_url = url
            if country_filter and "proxyscrape.com" in target_url and "country=all" in target_url:
                target_url = target_url.replace("country=all", f"country={country_filter.upper()}")
            target_urls.append((target_url, proto))

    c_info = f" (Country: {country_filter.upper()})" if country_filter else ""
    
    if HAS_HTTPX:
        batch_results = asyncio.run(fetch_all_proxies_httpx(target_urls, verbose, c_info))
    else:
        batch_results = fetch_all_proxies_threaded(target_urls, verbose, c_info)

    # Deduplicate
    seen_proxies: Set[str] = set()
    unique_candidates: List[Dict[str, str]] = []

    for batch in batch_results:
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

async def fetch_all_proxies(
    protocols: Optional[List[str]] = None, 
    country_filter: Optional[str] = None,
    config_path: Optional[str] = None,
    verbose: bool = True
) -> List[Dict[str, str]]:
    return fetch_proxies_sync(protocols=protocols, country_filter=country_filter, config_path=config_path, verbose=verbose)
