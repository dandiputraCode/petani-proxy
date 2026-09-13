"""
OmniProxy Harvester - Multi-Format Exporter
Exports verified alive proxies to TXT, JSON, CSV, and optional 9Router SQLite pool.
"""
import os
import csv
import json
import uuid
import sqlite3
import datetime
from typing import List, Dict, Any, Optional

def export_all_formats(
    live_proxies: List[Dict[str, Any]], 
    output_dir: Optional[str] = None, 
    sync_9router_db: Optional[str] = None
) -> Dict[str, str]:
    """
    Export verified proxies into TXT, JSON, and CSV in the designated output directory.
    Returns a dictionary of generated filepaths.
    """
    if not output_dir:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    generated_files = {}

    # 1. Plain Text Exporter (Categorized by protocol + unified all)
    by_proto = {"http": [], "socks4": [], "socks5": []}
    all_lines_raw = []
    all_lines_url = []

    for p in live_proxies:
        proto = p.get("protocol", "http").lower()
        proxy_raw = p["proxy"]
        proxy_url = f"{proto}://{proxy_raw}"
        
        all_lines_raw.append(proxy_raw)
        all_lines_url.append(proxy_url)
        if proto in by_proto:
            by_proto[proto].append(proxy_raw)

    # Save live_all.txt
    all_txt_path = os.path.join(output_dir, "live_all.txt")
    with open(all_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines_raw) + ("\n" if all_lines_raw else ""))
    generated_files["all_txt"] = all_txt_path

    # Save live_urls.txt
    all_url_path = os.path.join(output_dir, "live_urls.txt")
    with open(all_url_path, "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines_url) + ("\n" if all_lines_url else ""))
    generated_files["urls_txt"] = all_url_path

    # Save per-protocol txt files
    for proto, items in by_proto.items():
        proto_path = os.path.join(output_dir, f"live_{proto}.txt")
        with open(proto_path, "w", encoding="utf-8") as f:
            f.write("\n".join(items) + ("\n" if items else ""))
        generated_files[f"{proto}_txt"] = proto_path

    # 2. Rich JSON Exporter
    json_path = os.path.join(output_dir, "proxies.json")
    json_payload = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_alive": len(live_proxies),
        "protocols": {proto: len(items) for proto, items in by_proto.items()},
        "proxies": live_proxies
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_payload, f, indent=2)
    generated_files["json"] = json_path

    # 3. CSV Exporter
    csv_path = os.path.join(output_dir, "proxies.csv")
    fieldnames = [
        "protocol", "ip", "port", "proxy", "latency_ms", 
        "country_code", "country", "city", "isp", "egress_ip"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for p in live_proxies:
            writer.writerow(p)
    generated_files["csv"] = csv_path

    # 4. Optional 9Router SQLite Sync
    if sync_9router_db and os.path.exists(sync_9router_db):
        sync_to_9router(live_proxies, sync_9router_db)
        generated_files["9router_db"] = sync_9router_db

    return generated_files

def sync_to_9router(live_proxies: List[Dict[str, Any]], db_path: str, replace: bool = True):
    """Sync verified live proxies into 9Router SQLite database."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    if replace:
        cur.execute("DELETE FROM proxyPools WHERE data LIKE '%OmniProxy%' OR testStatus = 'unknown'")
        conn.commit()

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    inserted = 0

    for p in live_proxies:
        pid = str(uuid.uuid4())
        name = f"OmniProxy [{p.get('country_code', '??')}] {p['proxy']} ({p.get('protocol', 'http')})"
        proxy_url = f"{p.get('protocol', 'http')}://{p['proxy']}"
        payload = {
            "name": name,
            "proxyUrl": proxy_url,
            "noProxy": "",
            "type": p.get("protocol", "http"),
            "strictProxy": False,
            "lastTestedAt": now_iso,
            "lastError": None,
            "latency": p.get("latency_sec", 1.0),
            "egressIp": p.get("egress_ip", p["ip"]),
            "country": p.get("country_code", "??")
        }
        cur.execute("""
            INSERT INTO proxyPools (id, isActive, testStatus, data, createdAt, updatedAt)
            VALUES (?, 1, 'working', ?, ?, ?)
        """, (pid, json.dumps(payload), now_iso, now_iso))
        inserted += 1

    conn.commit()
    conn.close()
    return inserted
