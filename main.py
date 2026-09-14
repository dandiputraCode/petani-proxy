#!/usr/bin/env python3
"""
PetaniProxy v1.0
Pusat Amunisi Proxy Bersih, Segar & Berputar Otomatis (Local Rotating Gateway)
"""
import os
import sys
import time
import json
import argparse
import requests
from typing import Optional, List

# Force UTF-8 on Windows
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class DummyColor:
        def __getattr__(self, name):
            return ""
    Fore = Style = DummyColor()

from core.fetcher import fetch_proxies_sync
from core.checker import check_proxies_pool, DEFAULT_TEST_URL
from core.exporter import export_all_formats
from core.server import start_proxy_server
from core.updater import (
    get_local_version_info,
    check_for_updates,
    render_update_banner,
    show_full_announcement,
    perform_update
)

BANNER = f"""{Fore.CYAN}{Style.BRIGHT}
  ██████╗ ███████╗████████╗ █████╗ ███╗   ██╗██╗██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
  ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗████╗  ██║██║██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
  ██████╔╝█████╗     ██║   ███████║██╔██╗ ██║██║██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
  ██╔═══╝ ██╔══╝     ██║   ██╔══██║██║╚██╗██║██║██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
  ██║     ███████╗   ██║   ██║  ██║██║ ╚████║██║██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
  ╚═╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
{Fore.YELLOW}              🌾 PetaniProxy: Panen Proxy Cepat, Segar & Bergizi 🚜
{Fore.WHITE}          High-Speed Multi-Protocol Scraper, Validator & Local Gateway
{Fore.LIGHTBLACK_EX}                 Created & Maintained by {Fore.CYAN}@itzluthfi{Fore.LIGHTBLACK_EX} (github.com/itzluthfi)
{Style.RESET_ALL}"""

def find_9router_db() -> Optional[str]:
    """Smart auto-detection for BansosRouter / 9Router SQLite database."""
    env_path = os.environ.get("BANSOS_ROUTER_DB") or os.environ.get("NINEROUTER_DB")
    if env_path and os.path.exists(env_path):
        return env_path

    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.normpath(os.path.join(base_dir, "..", "9router-mibp-version", "data", "db", "data.sqlite")),
        os.path.normpath(os.path.join(base_dir, "..", "9router", "data", "db", "data.sqlite")),
        os.path.normpath(os.path.join(base_dir, "..", "bansos-router", "data", "db", "data.sqlite")),
        "D:/FREELANCE/9router-mibp-version/data/db/data.sqlite",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

def install_dependencies(quiet: bool = False) -> bool:
    """Auto-install or repair project dependencies using requirements.txt."""
    import subprocess
    print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}📦 MEMASANG DEPENDENSI PETANIPROXY...{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}Menjalankan: {sys.executable} -m pip install -r requirements.txt{Style.RESET_ALL}\n")
    req_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    cmd = [sys.executable, "-m", "pip", "install", "-r", req_file]
    if quiet:
        cmd.append("--quiet")
    res = subprocess.run(cmd)
    if res.returncode == 0:
        print(f"\n{Fore.GREEN}✓ Semua dependensi berhasil dipasang! Siap tempur! 🌾🚜{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")
        return True
    else:
        print(f"\n{Fore.RED}⚠️ Pemasangan paket selesai dengan beberapa catatan/peringatan.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")
        return False

def check_initial_dependencies() -> bool:
    """Smart check on first startup to ensure user has essential packages."""
    missing = []
    checks = [
        ("httpx", "httpx"),
        ("requests", "requests"),
        ("colorama", "colorama"),
        ("DrissionPage", "DrissionPage"),
        ("speech_recognition", "SpeechRecognition"),
        ("pydub", "pydub")
    ]
    for mod, pkg in checks:
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"\n{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}{Style.BRIGHT}📦 SETUP AWAL PETANIPROXY: Dependensi Belum Lengkap{Style.RESET_ALL}")
        print(f"  {Fore.LIGHTBLACK_EX}Terdeteksi beberapa paket yang belum terpasang di sistem Python kamu:{Style.RESET_ALL}")
        for m in missing:
            print(f"   {Fore.RED}•{Fore.WHITE} {m}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        ans = input(f"\n{Fore.CYAN}👉 Pasang semua dependensi otomatis sekarang (1-Klik via pip)? [Y/n]: {Style.RESET_ALL}").strip().lower()
        if ans in ("", "y", "yes"):
            return install_dependencies()
    return True

def find_grok_python() -> str:
    """Detect python executable for Grok Farm / Webshare Hunter."""
    candidates = [
        r"D:\FREELANCE\grok-register\venv\Scripts\python.exe",
        os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "grok-register", "venv", "Scripts", "python.exe")),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return sys.executable

def run_webshare_hunter(accounts: int = 1, headless: bool = True) -> bool:
    """Run Webshare Hunter to harvest residential clean proxies that bypass Cloudflare."""
    import subprocess
    grok_dir = r"D:\FREELANCE\grok-register"
    if not os.path.exists(grok_dir):
        grok_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "grok-register"))
    
    ws_script = os.path.join(grok_dir, "webshare_hunter_auto.py")
    if not os.path.exists(ws_script):
        print(f"{Fore.RED}❌ Script Webshare Hunter tidak ditemukan di {ws_script}{Style.RESET_ALL}")
        return False

    py_exec = find_grok_python()
    print(f"\n{Fore.CYAN}{'🏢 Menjalankan Webshare Residential Hunter...' if CURRENT_LANG == 'ID' else '🏢 Launching Webshare Residential Hunter...'}{Style.RESET_ALL}")
    print(f"  • Target: {Fore.YELLOW}{accounts} Akun Webshare ({accounts * 10} IP Residensial AS/Eropa){Style.RESET_ALL}")
    print(f"  • Mode:   {Fore.WHITE}{'Background (Headless)' if headless else 'Tampak Layar'}{Style.RESET_ALL}")
    print(f"  • Hasil:  {Fore.GREEN}Otomatis lolos Cloudflare xAI Grok & disetor ke proxies.txt + BansosRouter{Style.RESET_ALL}\n")

    cmd = [py_exec, ws_script, str(accounts)]
    if headless:
        cmd.append("--headless")

    try:
        res = subprocess.run(cmd, cwd=grok_dir)
        return res.returncode == 0
    except Exception as e:
        print(f"{Fore.RED}❌ Gagal menjalankan Webshare Hunter: {e}{Style.RESET_ALL}")
        return False

def print_live_proxy(proxy_res: dict, current_count: int, target: int):
    proto = proxy_res.get("protocol", "http").upper()
    lat = proxy_res.get("latency_ms", 0)
    proxy = proxy_res.get("proxy", "")
    cc = proxy_res.get("country_code", "??")
    country = proxy_res.get("country", "Unknown")
    isp = proxy_res.get("isp", "-")
    anon = proxy_res.get("anonymity", "Elite")
    
    # Anonymity badge styling
    if anon == "Elite":
        anon_badge = f"{Fore.CYAN}{Style.BRIGHT}[ELITE]{Style.RESET_ALL}"
    elif anon == "Anonymous":
        anon_badge = f"{Fore.MAGENTA}[ANON]{Style.RESET_ALL} "
    else:
        anon_badge = f"{Fore.YELLOW}[TRAN]{Style.RESET_ALL} "

    # Color based on latency
    if lat < 1000:
        lat_color = Fore.GREEN
    elif lat < 2500:
        lat_color = Fore.YELLOW
    else:
        lat_color = Fore.RED

    print(
        f"  {Fore.GREEN}🟢 [LIVE {current_count}/{target}]{Style.RESET_ALL} "
        f"{Fore.CYAN}{proto:<6}{Style.RESET_ALL} "
        f"{Fore.WHITE}{proxy:<21}{Style.RESET_ALL} | "
        f"{anon_badge} | "
        f"{lat_color}{lat:>4}ms{Style.RESET_ALL} | "
        f"{Fore.BLUE}[{cc}] {country:<13}{Style.RESET_ALL} | "
        f"{Fore.LIGHTBLACK_EX}{isp[:22]}{Style.RESET_ALL}"
    )

def run_harvester(
    protocols: list, 
    max_check: int = 200, 
    target_alive: int = 20, 
    timeout: float = 3.0, 
    workers: int = 50, 
    country: str = None, 
    anonymity: str = None,
    target_url: str = None,
    output_dir: str = None, 
    sync_9router: str = None,
    serve_port: int = None
):
    t_start = time.perf_counter()
    check_url = target_url or DEFAULT_TEST_URL
    print(f"\n{Fore.YELLOW}⚡ [1/3] Scraping raw candidates from open-source feeds...{Style.RESET_ALL}")
    candidates = fetch_proxies_sync(protocols=protocols, country_filter=country)
    
    if not candidates:
        print(f"{Fore.RED}❌ Gagal mengambil kandidat proxy dari feed.{Style.RESET_ALL}")
        return []

    url_hint = f" | Target: {check_url[:35]}" if target_url else ""
    anon_hint = f" | Anonymity: {anonymity.upper()}" if anonymity and anonymity.lower() != 'all' else ""
    print(f"\n{Fore.YELLOW}🔍 [2/3] Validating up to {max_check} candidates (Target alive: {target_alive}, Timeout: {timeout}s{url_hint}{anon_hint})...{Style.RESET_ALL}")
    
    live_proxies = check_proxies_pool(
        candidates=candidates,
        max_check=max_check,
        target_alive=target_alive,
        timeout=timeout,
        max_workers=workers,
        country_filter=country,
        anonymity_filter=anonymity,
        test_url=check_url,
        on_live_callback=print_live_proxy
    )

    elapsed_total = round(time.perf_counter() - t_start, 2)
    print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}🎉 Validation Complete! Found {len(live_proxies)} active proxies in {elapsed_total}s.{Style.RESET_ALL}")

    if not live_proxies:
        print(f"{Fore.YELLOW}⚠️ Tidak ada proxy yang lolos batas timeout {timeout}s. Coba perbesar --timeout atau perbanyak --max.{Style.RESET_ALL}")
        return []

    print(f"\n{Fore.YELLOW}💾 [3/3] Exporting verified proxies to disk...{Style.RESET_ALL}")
    files = export_all_formats(live_proxies, output_dir=output_dir, sync_9router_db=sync_9router)
    
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Plain Text:  {Fore.WHITE}{files.get('all_txt')}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} URLs Format: {Fore.WHITE}{files.get('urls_txt')}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Elite Only:  {Fore.WHITE}{files.get('elite_txt')}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Rich JSON:   {Fore.WHITE}{files.get('json')}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} CSV Sheet:   {Fore.WHITE}{files.get('csv')}{Style.RESET_ALL}")
    
    if "9router_db" in files:
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} BansosRouter DB: {Fore.WHITE}Synced to {files['9router_db']}{Style.RESET_ALL}")

    # Display Top 3 Fastest
    print(f"\n{Fore.CYAN}🏆 TOP FASTEST PROXIES:{Style.RESET_ALL}")
    for idx, p in enumerate(live_proxies[:3], 1):
        proto = p.get('protocol', 'http').upper()
        anon = p.get('anonymity', 'Elite')
        print(f"  {idx}. {Fore.GREEN}{proto}://{p['proxy']}{Style.RESET_ALL} [{anon}] ({p['latency_ms']}ms) - [{p['country_code']}] {p['country']}")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")

    if serve_port:
        print(f"{Fore.GREEN}{Style.BRIGHT}🌐 STARTING LOCAL ROTATING GATEWAY & REST API...{Style.RESET_ALL}")
        print(f"  • Forward Proxy Endpoint: {Fore.CYAN}http://127.0.0.1:{serve_port}{Style.RESET_ALL}")
        print(f"  • Random Proxy REST API:  {Fore.CYAN}http://127.0.0.1:{serve_port}/api/random{Style.RESET_ALL}")
        print(f"  • All Proxies REST API:   {Fore.CYAN}http://127.0.0.1:{serve_port}/api/all{Style.RESET_ALL}")
        print(f"  • Health & Status API:    {Fore.CYAN}http://127.0.0.1:{serve_port}/api/status{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}📋 SNIPPET SIAP PAKAI (COPY-PASTE):{Style.RESET_ALL}")
        print(f"  • {Fore.YELLOW}Python Requests:{Style.RESET_ALL} proxies={{'http': 'http://127.0.0.1:{serve_port}', 'https': 'http://127.0.0.1:{serve_port}'}}")
        print(f"  • {Fore.YELLOW}cURL Command:{Style.RESET_ALL}    curl -x http://127.0.0.1:{serve_port} https://api.ipify.org")
        print(f"  • {Fore.YELLOW}Browser Proxy:{Style.RESET_ALL}   Set Manual Proxy Host -> 127.0.0.1 | Port -> {serve_port}")
        print(f"\n{Fore.LIGHTBLACK_EX}Server running at 127.0.0.1:{serve_port}. Press Ctrl+C to stop.{Style.RESET_ALL}\n")
        start_proxy_server(live_proxies, host="127.0.0.1", port=serve_port, background=False)

    return live_proxies

def view_saved_results(output_dir: str = None):
    if not output_dir:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, "output")
    json_file = os.path.join(output_dir, "proxies.json")
    if not os.path.exists(json_file):
        print(f"\n{Fore.YELLOW}Belum ada riwayat hasil proxy tersimpan di {output_dir}. Jalankan harvest dulu!{Style.RESET_ALL}")
        return

    import json
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"\n{Fore.CYAN}📁 HASIL PROXY TERAKHIR DARI {json_file}:{Style.RESET_ALL}")
    print(f"  • Terakhir diperbarui: {Fore.WHITE}{data.get('generated_at', '-')}{Style.RESET_ALL}")
    print(f"  • Total proxy aktif  : {Fore.GREEN}{data.get('total_alive', 0)}{Style.RESET_ALL}")
    print(f"  • Protokol           : {Fore.WHITE}{data.get('protocols', {})}{Style.RESET_ALL}\n")

    proxies = data.get("proxies", [])
    print(f"{Fore.CYAN}DAFTAR 10 PROXY TERCEPAT:{Style.RESET_ALL}")
    for idx, p in enumerate(proxies[:10], 1):
        proto = p.get('protocol', 'http').upper()
        print(f"  {idx:>2}. {Fore.GREEN}{proto:<6}{Style.RESET_ALL} {Fore.WHITE}{p['proxy']:<21}{Style.RESET_ALL} | {Fore.YELLOW}{p['latency_ms']:>4}ms{Style.RESET_ALL} | [{p['country_code']}] {p['country']} ({p.get('isp', '-')[:22]})")

CURRENT_LANG = "ID"

def test_live_masking(port: int = 8888):
    """
    Fitur Pembuktian Langsung [T]:
    Uji apakah IP asli tertutup sempurna lewat Gateway 8888.
    """
    print(f"\n{Fore.CYAN}🧪 MEMERIKSA STATUS ANONIMITAS (LIVE MASKING TEST)...{Style.RESET_ALL}")
    
    # 1. Mendeteksi IP Asli
    print(f"  {Fore.LIGHTBLACK_EX}[1/2] Mendeteksi IP Asli perangkat kamu (Direct Connection)...{Style.RESET_ALL}")
    real_ip = "Unknown"
    real_isp = "Unknown"
    try:
        r = requests.get("https://ipwho.is/", timeout=5.0)
        if r.status_code == 200:
            d = r.json()
            real_ip = d.get("ip", "Unknown")
            real_isp = f"{d.get('connection', {}).get('isp', d.get('isp', '-'))} - {d.get('city', '-')}, {d.get('country', '-')}"
    except Exception:
        try:
            r = requests.get("https://api.ipify.org?format=json", timeout=4.0)
            real_ip = r.json().get("ip", "Unknown")
        except Exception:
            pass

    # 2. Menguji Gateway 127.0.0.1:8888
    print(f"  {Fore.LIGHTBLACK_EX}[2/2] Menguji koneksi lewat Rotating Gateway (127.0.0.1:{port})...{Style.RESET_ALL}")
    proxies = {
        "http": f"http://127.0.0.1:{port}",
        "https": f"http://127.0.0.1:{port}"
    }
    gateway_ip = None
    gateway_info = None
    try:
        r = requests.get("https://ipwho.is/", proxies=proxies, timeout=8.0)
        if r.status_code == 200:
            d = r.json()
            gateway_ip = d.get("ip")
            gateway_info = f"{d.get('connection', {}).get('isp', d.get('isp', '-'))} - {d.get('city', '-')}, {d.get('country', '-')}"
    except Exception:
        try:
            r = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=6.0)
            if r.status_code == 200:
                gateway_ip = r.json().get("ip")
        except Exception:
            pass

    print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}🛡️  HASIL AUDIT IDENTITAS & PRIVASI KONEKSI:{Style.RESET_ALL}")
    print(f"  • IP Asli Kamu     : {Fore.YELLOW}{real_ip}{Style.RESET_ALL} ({real_isp})")
    
    if gateway_ip:
        print(f"  • IP Masked Gateway: {Fore.GREEN}{Style.BRIGHT}{gateway_ip}{Style.RESET_ALL} ({gateway_info or 'Masked Proxy'})")
        if gateway_ip != real_ip:
            print(f"\n  {Fore.GREEN}{Style.BRIGHT}✅ STATUS: 100% AMAN & TERSAMARKAN! (ZERO LEAK){Style.RESET_ALL}")
            print(f"  {Fore.LIGHTBLACK_EX}Identitas asli kamu tertutup sempurna. Website target melihat kamu dari IP proxy.{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.RED}⚠️ STATUS: IP Gateway sama dengan IP asli. Periksa kembali konfigurasi proxy.{Style.RESET_ALL}")
    else:
        print(f"  • Gateway {port}     : {Fore.RED}Tidak aktif atau belum ada proxy hidup di pool.{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}💡 Tips: Jalankan salah satu Racikan [1-4] dulu untuk menyalakan Gateway {port}!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")

def show_manual_menu():
    """Sub-menu [M] Bengkel Oprek Manual untuk power user."""
    global CURRENT_LANG
    while True:
        print(BANNER)
        if CURRENT_LANG == "ID":
            m_box = f"""{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {Fore.WHITE}{Style.BRIGHT}🛠️  BENGKEL OPREK MANUAL (PETANIPROXY)
  {Fore.LIGHTBLACK_EX}Buat yang paham jeroan teknis — bebas atur protokol, filter & hook database
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  {Fore.GREEN}[1]{Fore.WHITE} ⚡ Quick Harvest Standar   {Fore.LIGHTBLACK_EX}Ambil 15 proxy tercepat dari semua tipe
  {Fore.GREEN}[2]{Fore.WHITE} 🔒 Khusus SOCKS5          {Fore.LIGHTBLACK_EX}Protokol tercepat & stabil (HTTP diskip)
  {Fore.GREEN}[3]{Fore.WHITE} 🌐 Khusus HTTP / HTTPS    {Fore.LIGHTBLACK_EX}Proxy klasik untuk web traffic biasa
  {Fore.GREEN}[4]{Fore.WHITE} 🌍 Filter Negara Tertentu {Fore.LIGHTBLACK_EX}Bebas ketik kode ISO (ID, SG, US, JP, dll)
  {Fore.GREEN}[5]{Fore.WHITE} 🛡️ Khusus Elite Proxies   {Fore.LIGHTBLACK_EX}High Anonymity Only — anti bocor header
  {Fore.GREEN}[6]{Fore.WHITE} 🎯 Tembak Target URL      {Fore.LIGHTBLACK_EX}Uji tembus domain incaran (contoh: x.ai)
  {Fore.GREEN}[7]{Fore.WHITE} 🏠 Nyalakan Gateway 8888  {Fore.LIGHTBLACK_EX}Host forward proxy & REST API lokal
  {Fore.GREEN}[8]{Fore.WHITE} 🔌 Setor ke BansosRouter  {Fore.LIGHTBLACK_EX}Inject proxy langsung ke database SQLite
  {Fore.GREEN}[9]{Fore.WHITE} 📦 Perbaiki Dependensi   {Fore.LIGHTBLACK_EX}Self-healing pip install requirements.txt
  {Fore.RED}[0]{Fore.WHITE} 🔙 Balik ke Menu Racikan  {Fore.LIGHTBLACK_EX}Kembali ke beranda utama

{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}"""
            prompt_str = f"{Fore.YELLOW}Pilih opsi Bengkel [1-9, 0=Kembali]: {Style.RESET_ALL}"
        else:
            m_box = f"""{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {Fore.WHITE}{Style.BRIGHT}🛠️  MANUAL TUNING WORKSHOP (PETANIPROXY)
  {Fore.LIGHTBLACK_EX}For power users who need custom protocols, filters & database hooks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  {Fore.GREEN}[1]{Fore.WHITE} ⚡ Standard Quick Sweep   {Fore.LIGHTBLACK_EX}Grab 15 fastest random live proxies
  {Fore.GREEN}[2]{Fore.WHITE} 🔒 Pure SOCKS5 Only       {Fore.LIGHTBLACK_EX}Ultra-fast SOCKS5 sockets only
  {Fore.GREEN}[3]{Fore.WHITE} 🌐 Classic HTTP / HTTPS   {Fore.LIGHTBLACK_EX}Standard HTTP browsing nodes
  {Fore.GREEN}[4]{Fore.WHITE} 🌍 Custom Country Filter  {Fore.LIGHTBLACK_EX}Filter by country ISO code (ID, SG, US...)
  {Fore.GREEN}[5]{Fore.WHITE} 🛡️ Elite Proxies Only     {Fore.LIGHTBLACK_EX}Strict ghost mode — zero header leaks
  {Fore.GREEN}[6]{Fore.WHITE} 🎯 Target-Specific Snipe  {Fore.LIGHTBLACK_EX}Probe directly against custom website/API
  {Fore.GREEN}[7]{Fore.WHITE} 🏠 Launch Local Gateway   {Fore.LIGHTBLACK_EX}Start rotating forward proxy on port 8888
  {Fore.GREEN}[8]{Fore.WHITE} 🔌 Sync BansosRouter DB   {Fore.LIGHTBLACK_EX}Feed live proxies into SQLite database pool
  {Fore.GREEN}[9]{Fore.WHITE} 📦 Repair Dependencies    {Fore.LIGHTBLACK_EX}Self-healing pip install requirements.txt
  {Fore.RED}[0]{Fore.WHITE} 🔙 Back to Presets Menu   {Fore.LIGHTBLACK_EX}Return to primary launcher

{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}"""
            prompt_str = f"{Fore.YELLOW}Select workshop option [1-9, 0=Back]: {Style.RESET_ALL}"

        print(m_box)
        try:
            choice = input(prompt_str).strip()
        except (KeyboardInterrupt, EOFError):
            break

        if choice in ("0", "b", "back", "q"):
            break
        elif choice == "1":
            q_str = f"{Fore.CYAN}{'Target proxy hidup [default: 15]: ' if CURRENT_LANG == 'ID' else 'Target alive count [default: 15]: '}{Style.RESET_ALL}"
            t_input = input(q_str).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max(250, target_val * 15), target_alive=target_val, timeout=3.0)
        elif choice == "2":
            q_str = f"{Fore.CYAN}{'Target SOCKS5 hidup [default: 15]: ' if CURRENT_LANG == 'ID' else 'Target SOCKS5 count [default: 15]: '}{Style.RESET_ALL}"
            t_input = input(q_str).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            run_harvester(protocols=["socks5"], max_check=max(250, target_val * 15), target_alive=target_val, timeout=3.0)
        elif choice == "3":
            q_str = f"{Fore.CYAN}{'Target HTTP hidup [default: 15]: ' if CURRENT_LANG == 'ID' else 'Target HTTP count [default: 15]: '}{Style.RESET_ALL}"
            t_input = input(q_str).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            run_harvester(protocols=["http"], max_check=max(250, target_val * 15), target_alive=target_val, timeout=3.0)
        elif choice == "4":
            cc_prompt = f"{Fore.CYAN}{'Kode negara ISO 2 huruf (contoh: ID, SG, US) [default: ID]: ' if CURRENT_LANG == 'ID' else 'Enter 2-letter Country Code [default: ID]: '}{Style.RESET_ALL}"
            cc = input(cc_prompt).strip() or "ID"
            t_prompt = f"{Fore.CYAN}{'Target proxy hidup [default: 5]: ' if CURRENT_LANG == 'ID' else 'Target alive count [default: 5]: '}{Style.RESET_ALL}"
            t_input = input(t_prompt).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 5
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max(350, target_val * 35), target_alive=target_val, country=cc, timeout=3.5)
        elif choice == "5":
            q_str = f"{Fore.CYAN}{'Target Elite proxy [default: 15]: ' if CURRENT_LANG == 'ID' else 'Target Elite count [default: 15]: '}{Style.RESET_ALL}"
            t_input = input(q_str).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max(350, target_val * 20), target_alive=target_val, anonymity="elite", timeout=3.0)
        elif choice == "6":
            u_prompt = f"{Fore.CYAN}{'URL target uji [default: https://google.com]: ' if CURRENT_LANG == 'ID' else 'Target URL [default: https://google.com]: '}{Style.RESET_ALL}"
            t_url = input(u_prompt).strip() or "https://google.com"
            t_prompt = f"{Fore.CYAN}{'Target proxy lolos [default: 10]: ' if CURRENT_LANG == 'ID' else 'Target alive count [default: 10]: '}{Style.RESET_ALL}"
            t_input = input(t_prompt).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 10
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max(400, target_val * 25), target_alive=target_val, target_url=t_url, timeout=3.5)
        elif choice == "7":
            port_prompt = f"{Fore.CYAN}{'Port gateway lokal [default: 8888]: ' if CURRENT_LANG == 'ID' else 'Local gateway port [default: 8888]: '}{Style.RESET_ALL}"
            port_input = input(port_prompt).strip()
            port_val = int(port_input) if port_input.isdigit() else 8888
            t_prompt = f"{Fore.CYAN}{'Jumlah proxy hidup di pool [default: 15]: ' if CURRENT_LANG == 'ID' else 'Target alive pool size [default: 15]: '}{Style.RESET_ALL}"
            t_input = input(t_prompt).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max(300, target_val * 15), target_alive=target_val, timeout=3.0, serve_port=port_val)
        elif choice == "8":
            detected_db = find_9router_db()
            hint = f" [Terdeteksi: {detected_db}]" if detected_db else ""
            custom_path = input(f"{Fore.CYAN}{'Path ke data.sqlite BansosRouter' + hint + ' [Enter untuk default]: ' if CURRENT_LANG == 'ID' else 'Enter BansosRouter data.sqlite path' + hint + ' [Enter for default]: '}{Style.RESET_ALL}").strip()
            db_target = custom_path if custom_path else detected_db
            if db_target and os.path.exists(db_target):
                run_harvester(protocols=["http", "socks4", "socks5"], max_check=250, target_alive=15, sync_9router=db_target)
            else:
                print(f"{Fore.RED}{'Database tidak ditemukan. Pastikan path benar.' if CURRENT_LANG == 'ID' else 'Database not found. Please verify path.'}{Style.RESET_ALL}")
        elif choice == "9":
            install_dependencies()
        else:
            print(f"{Fore.RED}{'Pilihan tidak valid.' if CURRENT_LANG == 'ID' else 'Invalid option.'}{Style.RESET_ALL}")

        try:
            pause_msg = "[Tekan Enter untuk kembali ke menu bengkel...]" if CURRENT_LANG == "ID" else "[Press Enter to return to workshop...]"
            input(f"\n{Fore.LIGHTBLACK_EX}{pause_msg}{Style.RESET_ALL}")
        except (KeyboardInterrupt, EOFError):
            break

def get_features_readiness(lang: str = "ID") -> dict:
    """Check readiness status of features, CapSolver balance, and compute system readiness progress bar."""
    import importlib.util
    import socket
    from core.webshare_hunter import check_capsolver_balance

    status = {}
    score = 0

    # 1. Dependensi Inti
    pkgs = ["httpx", "requests", "colorama", "DrissionPage", "speech_recognition", "pydub"]
    missing = [p for p in pkgs if importlib.util.find_spec(p) is None]
    if not missing:
        status["deps_badge"] = f"{Fore.GREEN}[OK ✓]{Style.RESET_ALL}"
        status["deps_desc"] = "DrissionPage, httpx, pydub, speech_recognition"
        score += 25
    else:
        status["deps_badge"] = f"{Fore.YELLOW}[KURANG: {len(missing)}]{Style.RESET_ALL}"
        status["deps_desc"] = f"Missing: {', '.join(missing)}"

    # 2. Webshare Hunter Audio Solver
    dp_found = importlib.util.find_spec("DrissionPage") is not None
    sr_found = importlib.util.find_spec("speech_recognition") is not None
    if dp_found and sr_found:
        status["webshare"] = f"{Fore.GREEN}[SIAP TEMPUR ✓]{Style.RESET_ALL}" if lang == "ID" else f"{Fore.GREEN}[READY ✓]{Style.RESET_ALL}"
        status["webshare_desc"] = "Free AI Audio Solver Aktif (Mode Jendela Tampak)" if lang == "ID" else "Free AI Audio Solver Active (Visible Window)"
        score += 25
    else:
        status["webshare"] = f"{Fore.YELLOW}[PERLU INSTALL]{Style.RESET_ALL}" if lang == "ID" else f"{Fore.YELLOW}[SETUP NEEDED]{Style.RESET_ALL}"
        status["webshare_desc"] = "Paket DrissionPage / speech_rec belum lengkap" if lang == "ID" else "Packages missing"

    # 3. CapSolver Engine (Headless capability)
    cs_info = check_capsolver_balance()
    status["capsolver_info"] = cs_info
    if cs_info.get("can_headless"):
        status["capsolver_badge"] = f"{Fore.GREEN}[SIAP ✓]{Style.RESET_ALL}" if lang == "ID" else f"{Fore.GREEN}[READY ✓]{Style.RESET_ALL}"
        status["capsolver_desc"] = f"Saldo: ${cs_info['balance']:.3f} (Headless Didukung Penuh)" if lang == "ID" else f"Balance: ${cs_info['balance']:.3f} (Headless Ready)"
        score += 20
    elif cs_info.get("has_key"):
        status["capsolver_badge"] = f"{Fore.YELLOW}[SALDO HABIS]{Style.RESET_ALL}" if lang == "ID" else f"{Fore.YELLOW}[EMPTY BALANCE]{Style.RESET_ALL}"
        status["capsolver_desc"] = f"Saldo ${cs_info['balance']:.3f} (Headless Off, Gunakan Free Audio)" if lang == "ID" else f"Balance ${cs_info['balance']:.3f} (Use Free Audio)"
        score += 10
    else:
        status["capsolver_badge"] = f"{Fore.LIGHTBLACK_EX}[TIDAK DIAKTIFKAN]{Style.RESET_ALL}" if lang == "ID" else f"{Fore.LIGHTBLACK_EX}[DISABLED]{Style.RESET_ALL}"
        status["capsolver_desc"] = "Key Kosong (Audio Solver Gratisan Tetap Aktif)" if lang == "ID" else "No Key (Free Audio Solver Remains Active)"
        score += 15

    # 4. 9Router DB sync
    db_path = find_9router_db()
    if db_path:
        status["sync"] = f"{Fore.GREEN}[9ROUTER LINKED]{Style.RESET_ALL}"
        status["db_desc"] = f"Terhubung ({os.path.basename(db_path)})" if lang == "ID" else f"Connected ({os.path.basename(db_path)})"
        score += 20
    else:
        status["sync"] = f"{Fore.CYAN}[STANDALONE]{Style.RESET_ALL}"
        status["db_desc"] = "Mode Mandiri (Database 9Router tidak terdeteksi)" if lang == "ID" else "Standalone mode"
        score += 10

    # 5. Gateway 8888 live port status
    gw_active = False
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.05)
            gw_active = (s.connect_ex(('127.0.0.1', 8888)) == 0)
    except Exception:
        gw_active = False

    if gw_active:
        status["gateway"] = f"{Fore.GREEN}[PORT 8888 AKTIF]{Style.RESET_ALL}" if lang == "ID" else f"{Fore.GREEN}[PORT 8888 ONLINE]{Style.RESET_ALL}"
    else:
        status["gateway"] = f"{Fore.RED}[BELUM AKTIF]{Style.RESET_ALL}" if lang == "ID" else f"{Fore.RED}[OFFLINE]{Style.RESET_ALL}"

    # 6. Storage count
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "output", "proxies.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                d = json.load(f)
                count = d.get("total_alive", 0)
                status["storage"] = f"{Fore.GREEN}[{count} PROXY TERSEDIA]{Style.RESET_ALL}" if lang == "ID" else f"{Fore.GREEN}[{count} PROXIES READY]{Style.RESET_ALL}"
                status["storage_desc"] = f"{count} Proxy Aktif Tersimpan di Disk" if lang == "ID" else f"{count} Active Proxies Stored"
                score += 15
        except Exception:
            status["storage"] = f"{Fore.GREEN}[READY]{Style.RESET_ALL}"
            status["storage_desc"] = "File penyimpanan siap"
            score += 10
    else:
        status["storage"] = f"{Fore.LIGHTBLACK_EX}[KOSONG]{Style.RESET_ALL}" if lang == "ID" else f"{Fore.LIGHTBLACK_EX}[EMPTY]{Style.RESET_ALL}"
        status["storage_desc"] = "Belum ada riwayat panen tersimpan" if lang == "ID" else "No saved proxies yet"
        score += 5

    pct = min(100, score)
    bar_len = 10
    filled = int(bar_len * pct / 100)
    bar_str = "█" * filled + "░" * (bar_len - filled)
    status["percent"] = pct
    status["bar"] = bar_str

    if pct >= 85:
        bar_color = Fore.GREEN
        state_txt = "Amunisi Siap Tempur!" if lang == "ID" else "Battle-Ready!"
    elif pct >= 60:
        bar_color = Fore.YELLOW
        state_txt = "Sebagian Siap" if lang == "ID" else "Partially Ready"
    else:
        bar_color = Fore.RED
        state_txt = "Perlu Setup" if lang == "ID" else "Setup Needed"

    status["progress_line"] = f"{bar_color}[{bar_str}] {pct}%{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}({state_txt}){Style.RESET_ALL}"
    return status

def show_interactive_menu():
    global CURRENT_LANG
    check_initial_dependencies()
    update_checked = False
    cached_update_info = None

    while True:
        # Check update once per app session (cached)
        if not update_checked:
            update_checked = True
            try:
                cached_update_info = check_for_updates(timeout=2.0)
            except Exception:
                cached_update_info = None

        print(BANNER)

        # Show update banner if new version is available!
        if cached_update_info and cached_update_info.get("has_update"):
            print(render_update_banner(cached_update_info, lang=CURRENT_LANG))
            print()

        local_info = get_local_version_info()
        local_ver = local_info.get("version", "1.0.0")
        st = get_features_readiness(lang=CURRENT_LANG)
        ready_label = f"{Fore.GREEN}[SIAP PAKAI]{Style.RESET_ALL}" if CURRENT_LANG == "ID" else f"{Fore.GREEN}[READY]{Style.RESET_ALL}"

        if CURRENT_LANG == "ID":
            u_line = f"  {Fore.YELLOW}{Style.BRIGHT}[U]{Fore.WHITE}{Style.BRIGHT} 🚀 Update Tersedia!       {Fore.GREEN}v{cached_update_info.get('remote_version')} [PILIH UNTUK UPDATE]\n" if (cached_update_info and cached_update_info.get("has_update")) else f"  {Fore.GREEN}[U]{Fore.WHITE} 🔄 Cek & Update Versi     {Fore.GREEN}[v{local_ver} TERBARU]{Style.RESET_ALL}\n"
            menu_box = f"""{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {Fore.WHITE}{Style.BRIGHT}🌾 PETANIPROXY v{local_ver} (PUSAT AMUNISI PROXY)
  {Fore.LIGHTBLACK_EX}Amunisi Proxy Anti-Tumbang, Siap Diajak Tempur 24/7 Gaspol!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  {Fore.WHITE}{Style.BRIGHT}📊 KESIAPAN AMUNISI : {st['progress_line']}
  {Fore.LIGHTBLACK_EX}├─ {Fore.WHITE}Dependensi Inti : {st['deps_badge']} {Fore.LIGHTBLACK_EX}{st['deps_desc']}
  {Fore.LIGHTBLACK_EX}├─ {Fore.WHITE}Webshare Hunter : {st['webshare']} {Fore.LIGHTBLACK_EX}{st['webshare_desc']}
  {Fore.LIGHTBLACK_EX}├─ {Fore.WHITE}CapSolver Engine: {st['capsolver_badge']} {Fore.LIGHTBLACK_EX}{st['capsolver_desc']}
  {Fore.LIGHTBLACK_EX}├─ {Fore.WHITE}BansosRouter DB : {st['sync']} {Fore.LIGHTBLACK_EX}{st['db_desc']}
  {Fore.LIGHTBLACK_EX}└─ {Fore.WHITE}Stok di Gudang  : {st['storage']} {Fore.LIGHTBLACK_EX}{st['storage_desc']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  {Fore.YELLOW}{Style.BRIGHT}⭐ [MVP] AMUNISI SULTAN: IP RESIDENTIAL (TEMBUS CLOUDFLARE)
  {Fore.YELLOW}{Style.BRIGHT}[W]{Fore.WHITE}{Style.BRIGHT} 🏢 Webshare Hunter Gacor   {st['webshare']} {Fore.YELLOW}(PILIHAN UTAMA MVP ⭐⭐⭐)
     {Fore.GREEN}└─ Auto-Solve Captcha Suara • IP Rumah Asli • 10-30 Proxy/Akun
     {Fore.LIGHTBLACK_EX}└─ Lolos Cloudflare, Grok AI, & provider bot AI ketat

  {Fore.MAGENTA}RACIKAN PROXY GRATISAN RAKYAT JELATA (GATEWAY PORT 8888)
  {Fore.GREEN}[1]{Fore.WHITE} 🐔 Racikan Ternak Akun    {st['sync']} {Fore.LIGHTBLACK_EX}Anti-limit buat Grok/Qoder
  {Fore.GREEN}[2]{Fore.WHITE} 🕷️ Racikan Scraper Barbar {ready_label} {Fore.LIGHTBLACK_EX}Pool 30+ IP, ganti IP tiap hit
  {Fore.GREEN}[3]{Fore.WHITE} ⚡ Racikan Ngacir Anti-Lag {ready_label} {Fore.LIGHTBLACK_EX}Ping <350ms, Node SG/ID/US
  {Fore.GREEN}[4]{Fore.WHITE} 🚜 Mode Petani AFK 24 Jam {ready_label} {Fore.LIGHTBLACK_EX}Tinggal tidur, muter 15 menit

  {Fore.MAGENTA}BUNGKUS HASIL PANEN & TES IDENTITAS
  {Fore.CYAN}[E]{Fore.WHITE} 📥 Bungkus File Mentah    {Fore.GREEN}[SIAP EKSPOR]{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}Sedot TXT, JSON, CSV buat bot lu
  {Fore.CYAN}[T]{Fore.WHITE} 🧪 Uji Kesaktian Topeng   {st['gateway']} {Fore.LIGHTBLACK_EX}Live Test kebocoran IP asli

  {Fore.MAGENTA}PEMBARUAN & BENGKEL OPREK
{u_line}  {Fore.YELLOW}[M]{Fore.WHITE} 🛠️ Oprek Suka-Suka        {ready_label} {Fore.LIGHTBLACK_EX}Racik protokol sendiri, pilih negara
  {Fore.YELLOW}[S]{Fore.WHITE} 📂 Gudang Amunisi         {st['storage']} {Fore.LIGHTBLACK_EX}Stok proxy segar tersimpan di disk
  {Fore.BLUE}[L]{Fore.WHITE} 🌐 Ganti Bahasa (EN/ID)   {Fore.LIGHTBLACK_EX}Currently: Bahasa Indonesia
  {Fore.RED}[0]{Fore.WHITE} 💀 Cabut Dulu (Rebahan)   {Fore.LIGHTBLACK_EX}Tutup laptop, ngopi dulu atau sentuh rumput

{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {Fore.LIGHTBLACK_EX}Maintainer: {Fore.YELLOW}@itzluthfi{Fore.LIGHTBLACK_EX}          Repository: {Fore.WHITE}github.com/itzluthfi
{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}"""
            prompt_str = f"{Fore.YELLOW}Pilih Opsi [W (MVP), 1-4, E, T, U, M, S, L, 0] (Saran: Pencet W aja udah paling mantap): {Style.RESET_ALL}"
        else:
            u_line = f"  {Fore.YELLOW}{Style.BRIGHT}[U]{Fore.WHITE}{Style.BRIGHT} 🚀 New Update Available!  {Fore.GREEN}v{cached_update_info.get('remote_version')} [SELECT TO UPDATE]\n" if (cached_update_info and cached_update_info.get("has_update")) else f"  {Fore.GREEN}[U]{Fore.WHITE} 🔄 Check & Update Version {Fore.GREEN}[v{local_ver} LATEST]{Style.RESET_ALL}\n"
            menu_box = f"""{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {Fore.WHITE}{Style.BRIGHT}🌾 PETANIPROXY v{local_ver} (ROTATING PROXY ARSENAL)
  {Fore.LIGHTBLACK_EX}Battle-Tested Rotating Proxy Ammo — Zero BS, 100% Free!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  {Fore.WHITE}{Style.BRIGHT}📊 SYSTEM READINESS : {st['progress_line']}
  {Fore.LIGHTBLACK_EX}├─ {Fore.WHITE}Core Dependencies: {st['deps_badge']} {Fore.LIGHTBLACK_EX}{st['deps_desc']}
  {Fore.LIGHTBLACK_EX}├─ {Fore.WHITE}Webshare Hunter  : {st['webshare']} {Fore.LIGHTBLACK_EX}{st['webshare_desc']}
  {Fore.LIGHTBLACK_EX}├─ {Fore.WHITE}CapSolver Engine : {st['capsolver_badge']} {Fore.LIGHTBLACK_EX}{st['capsolver_desc']}
  {Fore.LIGHTBLACK_EX}├─ {Fore.WHITE}BansosRouter DB  : {st['sync']} {Fore.LIGHTBLACK_EX}{st['db_desc']}
  {Fore.LIGHTBLACK_EX}└─ {Fore.WHITE}Ammo in Storage  : {st['storage']} {Fore.LIGHTBLACK_EX}{st['storage_desc']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  {Fore.YELLOW}{Style.BRIGHT}⭐ [MVP] S-TIER ARSENAL: GENUINE RESIDENTIAL POOL (CLOUDFLARE BYPASS)
  {Fore.YELLOW}{Style.BRIGHT}[W]{Fore.WHITE}{Style.BRIGHT} 🏢 Webshare Hunter Elite   {st['webshare']} {Fore.YELLOW}(MVP TOP PICK! ⭐⭐⭐)
     {Fore.GREEN}└─ Audio Captcha Solver • Real Residential IPs • 10-30 Nodes/Acc
     {Fore.LIGHTBLACK_EX}└─ Bypasses Cloudflare, Grok AI, & tight bot detection

  {Fore.MAGENTA}FREE PUBLIC ROTATING GATEWAY (LOCAL PORT 8888)
  {Fore.GREEN}[1]{Fore.WHITE} 🐔 Bot Breeder Rig        {st['sync']} {Fore.LIGHTBLACK_EX}Anti-ban tuned for Grok/Qoder
  {Fore.GREEN}[2]{Fore.WHITE} 🕷️ Barbaric Web Scraper   {ready_label} {Fore.LIGHTBLACK_EX}30+ pool, fresh IP every hit
  {Fore.GREEN}[3]{Fore.WHITE} ⚡ Ludicrous Speed Mode   {ready_label} {Fore.LIGHTBLACK_EX}Ping <350ms, Node SG/ID/US
  {Fore.GREEN}[4]{Fore.WHITE} 🚜 24/7 AFK Farmer Daemon {ready_label} {Fore.LIGHTBLACK_EX}Put your feet up, every 15m

  {Fore.MAGENTA}DUMP RAW AMMO & STEALTH TEST
  {Fore.CYAN}[E]{Fore.WHITE} 📥 Dump Raw Ammo Files    {Fore.GREEN}[READY TO DUMP]{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}Export TXT, JSON, CSV for bots
  {Fore.CYAN}[T]{Fore.WHITE} 🧪 Stealth Mask Check     {st['gateway']} {Fore.LIGHTBLACK_EX}Live test: Prove your real IP
 
  {Fore.MAGENTA}UPDATES & WORKSHOP
{u_line}  {Fore.YELLOW}[M]{Fore.WHITE} 🛠️ Custom Lab Workshop    {ready_label} {Fore.LIGHTBLACK_EX}Tweak protocols, filter ISO countries
  {Fore.YELLOW}[S]{Fore.WHITE} 📂 Ammo Storage Vault     {st['storage']} {Fore.LIGHTBLACK_EX}Check active proxies sitting on disk
  {Fore.BLUE}[L]{Fore.WHITE} 🌐 Switch Language (EN/ID){Fore.LIGHTBLACK_EX}Currently: English
  {Fore.RED}[0]{Fore.WHITE} 💀 Rage Quit              {Fore.LIGHTBLACK_EX}Close terminal, sip coffee & go touch grass

{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {Fore.LIGHTBLACK_EX}Maintainer: {Fore.YELLOW}@itzluthfi{Fore.LIGHTBLACK_EX}          Repository: {Fore.WHITE}github.com/itzluthfi
{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}"""
            prompt_str = f"{Fore.YELLOW}Select Option [W (MVP), 1-4, E, T, U, M, S, L, 0] (Pro-tip: Press W for godmode): {Style.RESET_ALL}"

        print(menu_box)
        try:
            choice = input(prompt_str).strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break

        if choice.lower() == "u":
            print(f"\n{Fore.CYAN}{'Memeriksa pembaruan ke GitHub...' if CURRENT_LANG == 'ID' else 'Checking GitHub for updates...'}{Style.RESET_ALL}")
            info = check_for_updates(timeout=3.5)
            if info.get("has_update"):
                print(render_update_banner(info, lang=CURRENT_LANG))
                show_full_announcement(info, lang=CURRENT_LANG)
                c_up = input(f"\n{Fore.YELLOW}{'Lakukan update sekarang? [Y/n]: ' if CURRENT_LANG == 'ID' else 'Perform update now? [Y/n]: '}{Style.RESET_ALL}").strip().lower()
                if c_up in ("", "y", "yes"):
                    perform_update(restart=True, lang=CURRENT_LANG)
            else:
                curr_ver = info.get("current_version", "1.0.0")
                print(f"\n{Fore.GREEN}✅ {'PetaniProxy sudah dalam versi paling baru' if CURRENT_LANG == 'ID' else 'PetaniProxy is up to date'} (v{curr_ver})!{Style.RESET_ALL}")
                show_full_announcement(info, lang=CURRENT_LANG)
            
            try:
                p_msg = "[Tekan Enter untuk kembali ke menu...]" if CURRENT_LANG == "ID" else "[Press Enter to return to main menu...]"
                input(f"\n{Fore.LIGHTBLACK_EX}{p_msg}{Style.RESET_ALL}")
            except (KeyboardInterrupt, EOFError):
                break
            continue

        if choice.lower() == "l":
            CURRENT_LANG = "EN" if CURRENT_LANG == "ID" else "ID"
            new_lang_name = "Bahasa Indonesia" if CURRENT_LANG == "ID" else "English"
            print(f"\n{Fore.GREEN}🌐 Bahasa antarmuka diubah ke: {new_lang_name}{Style.RESET_ALL}")
            continue

        if choice.lower() == "m":
            show_manual_menu()
            continue

        if choice.lower() == "t":
            test_live_masking(port=8888)
        elif choice.lower() == "e":
            q_str = f"{Fore.CYAN}{'Target jumlah proxy hidup yang mau diekspor [default: 20]: ' if CURRENT_LANG == 'ID' else 'Target alive proxies to export [default: 20]: '}{Style.RESET_ALL}"
            t_input = input(q_str).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 20
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max(250, target_val * 15), target_alive=target_val, timeout=3.0)
        elif choice == "" or choice == "1":
            print(f"\n{Fore.GREEN}{'🐔 Menjalankan Racikan Ternak Akun (Grok, Qoder & Bot AI)...' if CURRENT_LANG == 'ID' else '🐔 Launching Account Farming Preset (Grok, Qoder & AI)...'}{Style.RESET_ALL}")
            db_target = find_9router_db()
            if db_target:
                print(f"  {Fore.CYAN}✓ BansosRouter SQLite terdeteksi di: {Fore.WHITE}{db_target}{Style.RESET_ALL}")
            run_harvester(
                protocols=["http", "socks5"], 
                max_check=350, 
                target_alive=20, 
                anonymity="elite", 
                timeout=2.5, 
                serve_port=8888, 
                sync_9router=db_target
            )
        elif choice == "2":
            print(f"\n{Fore.GREEN}{'🕷️ Menjalankan Racikan Scraper Brutal (Shopee, Tokopedia, Web Data)...' if CURRENT_LANG == 'ID' else '🕷️ Launching Mass Web Scraper Preset...'}{Style.RESET_ALL}")
            run_harvester(
                protocols=["http", "socks4", "socks5"], 
                max_check=500, 
                target_alive=30, 
                anonymity="elite", 
                timeout=3.5, 
                serve_port=8888
            )
        elif choice == "3":
            print(f"\n{Fore.GREEN}{'⚡ Menjalankan Racikan Turbo Surfing (Ping Terendah, SG/ID/US)...' if CURRENT_LANG == 'ID' else '⚡ Launching Lightning Turbo Surfing Preset...'}{Style.RESET_ALL}")
            run_harvester(
                protocols=["http", "socks5"], 
                max_check=350, 
                target_alive=15, 
                timeout=2.0, 
                serve_port=8888
            )
        elif choice == "4":
            print(f"\n{Fore.MAGENTA}{'🚜 Mode Petani 24 Jam Aktif: Refresh berkala setiap 15 menit. Tekan Ctrl+C untuk berhenti.' if CURRENT_LANG == 'ID' else '🚜 24/7 Farmer Daemon Active: Auto-refreshing every 15 mins. Press Ctrl+C to stop.'}{Style.RESET_ALL}")
            while True:
                try:
                    db_target = find_9router_db()
                    run_harvester(
                        protocols=["http", "socks5"], 
                        max_check=300, 
                        target_alive=20, 
                        timeout=2.5, 
                        serve_port=8888,
                        sync_9router=db_target
                    )
                    time.sleep(15 * 60)
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}{'Mode Petani dihentikan.' if CURRENT_LANG == 'ID' else 'Farmer daemon stopped.'}{Style.RESET_ALL}")
                    break
        elif choice.lower() == "w":
            try:
                from core.webshare_hunter import run_webshare_hunter
            except ImportError as e:
                print(f"\n{Fore.RED}⚠️ Dependensi Webshare Hunter belum lengkap: {e}{Style.RESET_ALL}")
                ask_inst = input(f"{Fore.YELLOW}{'👉 Pasang otomatis sekarang (1-Klik via pip)? [Y/n]: ' if CURRENT_LANG == 'ID' else '👉 Auto-install dependencies now (1-Click via pip)? [Y/n]: '}{Style.RESET_ALL}").strip().lower()
                if ask_inst in ("", "y", "yes"):
                    if install_dependencies():
                        try:
                            from core.webshare_hunter import run_webshare_hunter
                        except ImportError:
                            print(f"{Fore.RED}{'Gagal memuat Webshare Hunter setelah instalasi.' if CURRENT_LANG == 'ID' else 'Failed to load Webshare Hunter after installation.'}{Style.RESET_ALL}")
                            continue
                    else:
                        continue
                else:
                    continue

            print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'⭐ MEMBUKA WEBSHARE RESIDENTIAL HUNTER (FITUR MVP)...' if CURRENT_LANG == 'ID' else '⭐ LAUNCHING WEBSHARE RESIDENTIAL HUNTER (MVP FEATURE)...'}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLACK_EX}{'💡 Info: 1 Akun Webshare menghasilkan 10 IP Residential asli dengan username:password pribadi.' if CURRENT_LANG == 'ID' else '💡 Info: 1 Webshare account generates 10 genuine Residential IPs with private credentials.'}{Style.RESET_ALL}")
            acc_prompt = f"{Fore.CYAN}{'Berapa akun Webshare yang ingin dipanen? [Default: 1]: ' if CURRENT_LANG == 'ID' else 'How many Webshare accounts to hunt? [Default: 1]: '}{Style.RESET_ALL}"
            a_input = input(acc_prompt).strip()
            total_acc = int(a_input) if a_input.isdigit() and int(a_input) > 0 else 1

            from core.webshare_hunter import check_capsolver_balance
            cs_info = check_capsolver_balance()
            is_headless = False

            if cs_info.get("can_headless"):
                print(f"\n  {Fore.GREEN}✓ CapSolver API Aktif! Saldo: ${cs_info['balance']:.3f} (Mode Headless siap tempur){Style.RESET_ALL}")
                head_prompt = f"{Fore.CYAN}{'Jalankan di background tanpa jendela (Headless)? [Y/n]: ' if CURRENT_LANG == 'ID' else 'Run in background (Headless)? [Y/n]: '}{Style.RESET_ALL}"
                h_input = input(head_prompt).strip().lower()
                is_headless = h_input in ("", "y", "yes")
            else:
                print(f"\n{Fore.CYAN}ℹ️  STATUS ENGINE CAPTCHA & MODE TAMPILAN:{Style.RESET_ALL}")
                print(f"  • Solver Aktif   : {Fore.GREEN}Free AI Audio Solver (SpeechRecognition, Tanpa Saldo Token){Style.RESET_ALL}")
                print(f"  • Status Headless: {Fore.YELLOW}Dimatikan Otomatis{Style.RESET_ALL} ({cs_info.get('message')})")
                print(f"  {Fore.LIGHTBLACK_EX}💡 Penjelasan: Audio Solver gratisan WAJIB menggunakan jendela tampak agar bot")
                print(f"     bergerak alami & tidak diblokir 'Automated queries' oleh Google reCAPTCHA.{Style.RESET_ALL}")
                print(f"  {Fore.GREEN}👉 Otomatis menggunakan Mode Jendela Tampak (Mode Paling Stabil & Gacor)...{Style.RESET_ALL}\n")
                is_headless = False

            db_target = find_9router_db()
            run_webshare_hunter(total=total_acc, headless=is_headless, sync_9router_db=db_target)
        elif choice.lower() in ("s", "saved"):
            view_saved_results()
        elif choice == "0" or choice.lower() == "q":
            goodbye_msg = "💀 Capek panen, cabut dulu ah... Jangan lupa sentuh rumput bos! 👋" if CURRENT_LANG == "ID" else "💀 Session terminated — go touch some grass! 👋"
            print(f"\n{Fore.YELLOW}{goodbye_msg}{Style.RESET_ALL}\n")
            break
        else:
            invalid_msg = "Pilihan tidak valid. Silakan pilih 1-4, E, T, M, S, L, atau 0." if CURRENT_LANG == "ID" else "Invalid option. Please choose 1-4, E, T, M, S, L, or 0."
            print(f"{Fore.RED}{invalid_msg}{Style.RESET_ALL}")

        try:
            pause_msg = "[Tekan Enter untuk kembali ke menu utama...]" if CURRENT_LANG == "ID" else "[Press Enter to return to main menu...]"
            input(f"\n{Fore.LIGHTBLACK_EX}{pause_msg}{Style.RESET_ALL}")
        except (KeyboardInterrupt, EOFError):
            break

def main():
    if len(sys.argv) == 1:
        show_interactive_menu()
        return

    parser = argparse.ArgumentParser(description="PetaniProxy v1.0 - High-Speed Multi-Protocol Proxy Harvester & Rotating Gateway")
    parser.add_argument("--protocol", "-p", choices=["all", "http", "socks4", "socks5"], default="all", help="Target proxy protocol (default: all)")
    parser.add_argument("--max", "-m", type=int, default=250, help="Maximum candidate proxies to validate (default: 250)")
    parser.add_argument("--target", "-t", type=int, default=15, help="Target number of alive proxies to collect (default: 15)")
    parser.add_argument("--timeout", type=float, default=3.0, help="Connection timeout in seconds (default: 3.0)")
    parser.add_argument("--workers", "-w", type=int, default=50, help="Concurrent testing workers (default: 50)")
    parser.add_argument("--country", "-c", type=str, default=None, help="Filter by country ISO code (e.g. US, SG, ID, DE)")
    parser.add_argument("--anonymity", choices=["all", "elite", "anonymous", "transparent"], default="all", help="Filter by anonymity level (default: all)")
    parser.add_argument("--target-url", type=str, default=None, help="Validate proxies against specific website (e.g. https://google.com)")
    parser.add_argument("--serve", nargs="?", const=8888, type=int, default=None, help="Start local rotating forward proxy & REST API on port (default: 8888)")
    parser.add_argument("--loop", "-l", type=int, default=0, help="Auto-refresh loop interval in minutes (0 = single run)")
    parser.add_argument("--output", "-o", type=str, default=None, help="Custom output directory")
    parser.add_argument("--sync-9router", type=str, default=None, help="Path to BansosRouter/9Router data.sqlite for direct database sync (or 'auto')")
    parser.add_argument("--webshare", "-W", type=int, nargs="?", const=1, default=None, help="Trigger Webshare Residential Hunter for N accounts (default: 1)")
    parser.add_argument("--headless", action="store_true", help="Run Webshare Hunter in headless mode")
    parser.add_argument("--update", action="store_true", help="Perform 1-click update via git pull and exit")
    parser.add_argument("--check-update", action="store_true", help="Check for available updates on GitHub and display patch notes")
    parser.add_argument("--install-deps", action="store_true", help="Auto-install all dependencies from requirements.txt")
    parser.add_argument("--version", "-v", action="store_true", help="Show current version, announcement and exit")

    args = parser.parse_args()

    if args.version:
        v_info = get_local_version_info()
        print(BANNER)
        show_full_announcement(v_info)
        return

    if args.install_deps:
        print(BANNER)
        install_dependencies()
        return

    if args.check_update:
        print(BANNER)
        print(f"{Fore.CYAN}Memeriksa pembaruan ke GitHub...{Style.RESET_ALL}\n")
        info = check_for_updates(timeout=3.5)
        if info.get("has_update"):
            print(render_update_banner(info))
            show_full_announcement(info)
        else:
            print(f"{Fore.GREEN}✅ PetaniProxy sudah versi terbaru (v{info.get('current_version')})!{Style.RESET_ALL}")
            show_full_announcement(info)
        return

    if args.update:
        print(BANNER)
        perform_update(restart=False)
        return

    print(BANNER)

    router_db = args.sync_9router
    if router_db == "auto" or router_db is None:
        router_db = find_9router_db()

    if args.webshare is not None:
        try:
            from core.webshare_hunter import run_webshare_hunter, check_capsolver_balance
        except ImportError as e:
            print(f"{Fore.RED}⚠️ Dependensi Webshare Hunter belum lengkap: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Silakan jalankan: python main.py --install-deps{Style.RESET_ALL}\n")
            sys.exit(1)

        if args.headless:
            cs = check_capsolver_balance()
            if not cs.get("can_headless"):
                print(f"\n{Fore.YELLOW}⚠️ PERINGATAN HEADLESS:{Style.RESET_ALL} {cs.get('message')}")
                print(f"{Fore.LIGHTBLACK_EX}Menjalankan Audio Solver gratisan di mode headless berisiko tinggi memicu blokir 'Automated queries' dari Google.")
                print(f"Disarankan menjalankan tanpa flag --headless atau sediakan CAPSOLVER_API_KEY.{Style.RESET_ALL}\n")

        run_webshare_hunter(total=args.webshare, headless=args.headless, sync_9router_db=router_db, output_dir=args.output)
        return

    proto_list = [args.protocol] if args.protocol != "all" else ["http", "socks4", "socks5"]

    if args.loop > 0:
        print(f"{Fore.MAGENTA}🔄 Auto-refresh loop active: Running every {args.loop} minutes... (Press Ctrl+C to stop){Style.RESET_ALL}")
        while True:
            try:
                run_harvester(
                    protocols=proto_list,
                    max_check=args.max,
                    target_alive=args.target,
                    timeout=args.timeout,
                    workers=args.workers,
                    country=args.country,
                    anonymity=args.anonymity,
                    target_url=args.target_url,
                    output_dir=args.output,
                    sync_9router=router_db,
                    serve_port=args.serve
                )
                print(f"{Fore.LIGHTBLACK_EX}Sleeping for {args.loop} minutes before next sweep...{Style.RESET_ALL}")
                time.sleep(args.loop * 60)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}🛑 Harvester stopped by user.{Style.RESET_ALL}")
                break
    else:
        run_harvester(
            protocols=proto_list,
            max_check=args.max,
            target_alive=args.target,
            timeout=args.timeout,
            workers=args.workers,
            country=args.country,
            anonymity=args.anonymity,
            target_url=args.target_url,
            output_dir=args.output,
            sync_9router=router_db,
            serve_port=args.serve
        )

if __name__ == "__main__":
    main()
