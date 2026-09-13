#!/usr/bin/env python3
"""
OmniProxy Harvester
High-Speed Multi-Protocol Open-Source Proxy Harvester & Validator
"""
import os
import sys
import time
import argparse

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

BANNER = f"""{Fore.CYAN}{Style.BRIGHT}
  ██████╗ ███╗   ███╗███╗   ██╗██╗██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
 ██╔═══██╗████╗ ████║████╗  ██║██║██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
 ██║   ██║██╔████╔██║██╔██╗ ██║██║██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
 ██║   ██║██║╚██╔╝██║██║╚██╗██║██║██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
 ╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
{Fore.WHITE}      High-Speed Multi-Protocol Open-Source Proxy Harvester & Validator
{Fore.YELLOW}                  [HTTP • HTTPS • SOCKS4 • SOCKS5 • GeoIP]
{Fore.LIGHTBLACK_EX}             Created & Maintained by {Fore.CYAN}@itzluthfi{Fore.LIGHTBLACK_EX} (github.com/itzluthfi)
{Style.RESET_ALL}"""

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
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} 9Router DB:  {Fore.WHITE}Synced to {files['9router_db']}{Style.RESET_ALL}")

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

def show_presets_menu():
    global CURRENT_LANG
    while True:
        print(BANNER)
        if CURRENT_LANG == "ID":
            p_box = f"""{Fore.CYAN}┌────────────────────────────────────────────────────────────────────────┐
│                   {Fore.WHITE}{Style.BRIGHT}🎯 PRESET USE-CASE (TINGGAL GAS!){Fore.CYAN}                    │
│           {Fore.LIGHTBLACK_EX}Setup racikan siap pakai untuk kebutuhan bot & scraper{Fore.CYAN}       │
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.GREEN}[1]{Fore.WHITE} 🤖 AI & LLM Bot Mode    {Fore.LIGHTBLACK_EX}Biar bot AI kamu gak kena limit rate API    {Fore.CYAN}│
│  {Fore.GREEN}[2]{Fore.WHITE} 🕷 Mass Web Scraper     {Fore.LIGHTBLACK_EX}Khusus scraper brutal, anti kena banned IP  {Fore.CYAN}│
│  {Fore.GREEN}[3]{Fore.WHITE} 🌍 SEO & Geo-Target     {Fore.LIGHTBLACK_EX}Cek tampang Google dari sudut pandang asing {Fore.CYAN}│
│  {Fore.GREEN}[4]{Fore.WHITE} 🛡 Browser Privacy      {Fore.LIGHTBLACK_EX}Bypass internet positif tanpa perlu VPN     {Fore.CYAN}│
│  {Fore.RED}[0]{Fore.WHITE} 🔙 Balik ke Menu        {Fore.LIGHTBLACK_EX}Gak jadi deh, balik ke menu utama           {Fore.CYAN}│
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.LIGHTBLACK_EX}Maintainer: {Fore.YELLOW}@itzluthfi{Fore.LIGHTBLACK_EX}          Repository: {Fore.WHITE}github.com/itzluthfi{Fore.CYAN}       │
└────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}"""
            prompt_str = f"{Fore.YELLOW}Pilih preset [1-4, 0=Kembali]: {Style.RESET_ALL}"
        else:
            p_box = f"""{Fore.CYAN}┌────────────────────────────────────────────────────────────────────────┐
│                  {Fore.WHITE}{Style.BRIGHT}🎯 ONE-CLICK PRESET MODES (PLUG & PLAY){Fore.CYAN}               │
│          {Fore.LIGHTBLACK_EX}Pre-tuned battle setups for common developer workflows{Fore.CYAN}       │
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.GREEN}[1]{Fore.WHITE} 🤖 AI & LLM Bot Mode    {Fore.LIGHTBLACK_EX}Keep your AI bots alive without rate limits {Fore.CYAN}│
│  {Fore.GREEN}[2]{Fore.WHITE} 🕷 Mass Web Scraper     {Fore.LIGHTBLACK_EX}Brutal scraper setup, 100% leak-proof Elite {Fore.CYAN}│
│  {Fore.GREEN}[3]{Fore.WHITE} 🌍 SEO & Geo-Target     {Fore.LIGHTBLACK_EX}Audit localized Google SERPs from abroad    {Fore.CYAN}│
│  {Fore.GREEN}[4]{Fore.WHITE} 🛡 Browser Privacy      {Fore.LIGHTBLACK_EX}Unblock restricted dev sites without VPN    {Fore.CYAN}│
│  {Fore.RED}[0]{Fore.WHITE} 🔙 Back to Main Menu    {Fore.LIGHTBLACK_EX}Nevermind, take me back to safety           {Fore.CYAN}│
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.LIGHTBLACK_EX}Maintainer: {Fore.YELLOW}@itzluthfi{Fore.LIGHTBLACK_EX}          Repository: {Fore.WHITE}github.com/itzluthfi{Fore.CYAN}       │
└────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}"""
            prompt_str = f"{Fore.YELLOW}Select preset [1-4, 0=Back]: {Style.RESET_ALL}"

        print(p_box)
        try:
            choice = input(prompt_str).strip()
        except (KeyboardInterrupt, EOFError):
            break

        if choice == "1":
            print(f"\n{Fore.GREEN}{'🤖 Menjalankan Preset AI & LLM Bot Rotator...' if CURRENT_LANG == 'ID' else '🤖 Launching AI & LLM Bot Rotator Preset...'}{Style.RESET_ALL}")
            possible_path = "D:/FREELANCE/9router-mibp-version/data/db/data.sqlite"
            db = possible_path if os.path.exists(possible_path) else None
            run_harvester(protocols=["http", "socks5"], max_check=350, target_alive=20, timeout=2.5, serve_port=8888, sync_9router=db)
        elif choice == "2":
            print(f"\n{Fore.GREEN}{'🕷️ Menjalankan Preset Mass Web Scraper (Mode Brutal)...' if CURRENT_LANG == 'ID' else '🕷️ Launching Mass Web Scraper Preset...'}{Style.RESET_ALL}")
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=500, target_alive=30, anonymity="elite", timeout=3.0, serve_port=8888)
        elif choice == "3":
            cc_prompt = f"{Fore.CYAN}{'Masukkan kode negara target (default: US): ' if CURRENT_LANG == 'ID' else 'Enter target country for SEO audit [default: US]: '}{Style.RESET_ALL}"
            cc = input(cc_prompt).strip() or "US"
            print(f"\n{Fore.GREEN}{'🌍 Menjalankan Preset SEO & Geo-Target untuk' if CURRENT_LANG == 'ID' else '🌍 Launching SEO & Geo-Target Preset for'} [{cc}]...{Style.RESET_ALL}")
            run_harvester(protocols=["http", "socks5"], max_check=400, target_alive=10, country=cc, target_url="https://google.com", timeout=3.5)
        elif choice == "4":
            print(f"\n{Fore.GREEN}{'🛡️ Menjalankan Preset Privacy & Anti Internet Positif...' if CURRENT_LANG == 'ID' else '🛡️ Launching Browser Privacy & Unblocker Preset...'}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'💡 Tips: Pasang proxy di browser/komputer kamu ke 127.0.0.1:8888!' if CURRENT_LANG == 'ID' else '💡 Tip: Configure your browser proxy to 127.0.0.1:8888!'}{Style.RESET_ALL}")
            run_harvester(protocols=["http", "socks5"], max_check=300, target_alive=10, country="SG", timeout=2.5, serve_port=8888)
        elif choice in ("0", "b", "back", "q"):
            break
        else:
            print(f"{Fore.RED}{'Pilihan preset tidak valid.' if CURRENT_LANG == 'ID' else 'Invalid preset choice.'}{Style.RESET_ALL}")

        try:
            input(f"\n{Fore.LIGHTBLACK_EX}[{'Tekan Enter untuk kembali ke menu preset...' if CURRENT_LANG == 'ID' else 'Press Enter to return to Presets menu...'}]{Style.RESET_ALL}")
        except (KeyboardInterrupt, EOFError):
            break

def show_interactive_menu():
    global CURRENT_LANG
    while True:
        print(BANNER)
        if CURRENT_LANG == "ID":
            menu_box = f"""{Fore.CYAN}┌────────────────────────────────────────────────────────────────────────┐
│                    {Fore.WHITE}{Style.BRIGHT}OMNIPROXY HARVESTER MENU (INDONESIA){Fore.CYAN}                │
│                 {Fore.LIGHTBLACK_EX}High-Speed Multi-Protocol Scraper & Validator{Fore.CYAN}          │
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.MAGENTA}[P]{Fore.WHITE} 🎯 Preset Mode         {Fore.LIGHTBLACK_EX}Mode siap pakai: AI Bot, Scraper & Privacy   {Fore.CYAN}│
│  {Fore.GREEN}[1]{Fore.WHITE} ⚡ Quick Harvest       {Fore.LIGHTBLACK_EX}Cari 15 proxy tercepat dari semua protokol   {Fore.CYAN}│
│  {Fore.GREEN}[2]{Fore.WHITE} 🔒 SOCKS5 Only        {Fore.LIGHTBLACK_EX}Khusus SOCKS5 — HTTP disuruh minggir dulu    {Fore.CYAN}│
│  {Fore.GREEN}[3]{Fore.WHITE} 🌐 HTTP / HTTPS       {Fore.LIGHTBLACK_EX}Cari & validasi proxy untuk web browsing     {Fore.CYAN}│
│  {Fore.GREEN}[4]{Fore.WHITE} 🌍 Target Negara      {Fore.LIGHTBLACK_EX}Filter proxy berdasarkan kode negara / ISO   {Fore.CYAN}│
│  {Fore.GREEN}[5]{Fore.WHITE} 🛡 Elite Proxies      {Fore.LIGHTBLACK_EX}Hanya proxy high-anonymity, IP jangan bocor! {Fore.CYAN}│
│  {Fore.GREEN}[6]{Fore.WHITE} 🎯 Target-Specific    {Fore.LIGHTBLACK_EX}Tes proxy ke URL / target yang kamu tentukan {Fore.CYAN}│
│  {Fore.GREEN}[7]{Fore.WHITE} 🏠 Local Server       {Fore.LIGHTBLACK_EX}Jalankan proxy server & REST API lokal       {Fore.CYAN}│
│  {Fore.GREEN}[8]{Fore.WHITE} 🔄 Auto-Refresh       {Fore.LIGHTBLACK_EX}Panen ulang otomatis setiap N menit          {Fore.CYAN}│
│  {Fore.GREEN}[9]{Fore.WHITE} 🔌 Sync to 9Router    {Fore.LIGHTBLACK_EX}Setor proxy tervalidasi ke database 9Router  {Fore.CYAN}│
│  {Fore.GREEN}[S]{Fore.WHITE} 📂 Saved Output       {Fore.LIGHTBLACK_EX}Cek hasil panen yang sudah tersimpan di disk {Fore.CYAN}│
│  {Fore.CYAN}[L]{Fore.WHITE} 🌐 Switch Language    {Fore.LIGHTBLACK_EX}Ganti bahasa ke English                      {Fore.CYAN}│
│  {Fore.RED}[0]{Fore.WHITE} 💀 Exit Program       {Fore.LIGHTBLACK_EX}Keluar dari sistem — pelayanan selesai       {Fore.CYAN}│
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.LIGHTBLACK_EX}Maintainer: {Fore.YELLOW}@itzluthfi{Fore.LIGHTBLACK_EX}          Repository: {Fore.WHITE}github.com/itzluthfi{Fore.CYAN}       │
└────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}"""
            prompt_str = f"{Fore.YELLOW}Pilih opsi [P, 0-9, S, L] (Default: 1): {Style.RESET_ALL}"
        else:
            menu_box = f"""{Fore.CYAN}┌────────────────────────────────────────────────────────────────────────┐
│                     {Fore.WHITE}{Style.BRIGHT}OMNIPROXY HARVESTER MENU (ENGLISH){Fore.CYAN}                 │
│                 {Fore.LIGHTBLACK_EX}High-Speed Multi-Protocol Scraper & Validator{Fore.CYAN}          │
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.MAGENTA}[P]{Fore.WHITE} 🎯 Preset Modes       {Fore.LIGHTBLACK_EX}Pre-tuned battle setups for scrapers & bots  {Fore.CYAN}│
│  {Fore.GREEN}[1]{Fore.WHITE} ⚡ Quick Harvest       {Fore.LIGHTBLACK_EX}Find fastest proxies before coffee gets cold {Fore.CYAN}│
│  {Fore.GREEN}[2]{Fore.WHITE} 🔒 SOCKS5 Only        {Fore.LIGHTBLACK_EX}Pure SOCKS5 speed — tell HTTP to take a hike {Fore.CYAN}│
│  {Fore.GREEN}[3]{Fore.WHITE} 🌐 HTTP / HTTPS       {Fore.LIGHTBLACK_EX}Classic browsing nodes for normal human web  {Fore.CYAN}│
│  {Fore.GREEN}[4]{Fore.WHITE} 🌍 Target Country     {Fore.LIGHTBLACK_EX}Pick your proxy nationality (US, SG, ID, etc){Fore.CYAN}│
│  {Fore.GREEN}[5]{Fore.WHITE} 🛡 Elite Proxies      {Fore.LIGHTBLACK_EX}Ghost mode on — zero IP or header leaks!     {Fore.CYAN}│
│  {Fore.GREEN}[6]{Fore.WHITE} 🎯 Target-Specific    {Fore.LIGHTBLACK_EX}Snipe a specific website (Google, Shop, etc) {Fore.CYAN}│
│  {Fore.GREEN}[7]{Fore.WHITE} 🏠 Local Server       {Fore.LIGHTBLACK_EX}Host your own rotating gateway on port 8888  {Fore.CYAN}│
│  {Fore.GREEN}[8]{Fore.WHITE} 🔄 Auto-Refresh       {Fore.LIGHTBLACK_EX}Infinite loop harvest while you take a nap   {Fore.CYAN}│
│  {Fore.GREEN}[9]{Fore.WHITE} 🔌 Sync to 9Router    {Fore.LIGHTBLACK_EX}Feed live proxies into 9Router SQLite pool   {Fore.CYAN}│
│  {Fore.GREEN}[S]{Fore.WHITE} 📂 Saved Output       {Fore.LIGHTBLACK_EX}Inspect the goodies you just harvested       {Fore.CYAN}│
│  {Fore.CYAN}[L]{Fore.WHITE} 🌐 Switch Language    {Fore.LIGHTBLACK_EX}Ganti bahasa ke Bahasa Indonesia             {Fore.CYAN}│
│  {Fore.RED}[0]{Fore.WHITE} 💀 Exit Program       {Fore.LIGHTBLACK_EX}Aight imma head out — session terminated     {Fore.CYAN}│
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.LIGHTBLACK_EX}Maintainer: {Fore.YELLOW}@itzluthfi{Fore.LIGHTBLACK_EX}          Repository: {Fore.WHITE}github.com/itzluthfi{Fore.CYAN}       │
└────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}"""
            prompt_str = f"{Fore.YELLOW}Select option [P, 0-9, S, L] (Default: 1): {Style.RESET_ALL}"

        print(menu_box)
        try:
            choice = input(prompt_str).strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break

        if choice.lower() == "l":
            CURRENT_LANG = "EN" if CURRENT_LANG == "ID" else "ID"
            new_lang_name = "Bahasa Indonesia" if CURRENT_LANG == "ID" else "English"
            print(f"\n{Fore.GREEN}🌐 Bahasa antarmuka diubah ke: {new_lang_name}{Style.RESET_ALL}")
            continue

        if choice.lower() == "p":
            show_presets_menu()
            continue

        if choice == "" or choice == "1":
            q_str = f"{Fore.CYAN}{'Mau panen berapa proxy hidup? [default: 15]: ' if CURRENT_LANG == 'ID' else 'Target alive proxies count [default: 15]: '}{Style.RESET_ALL}"
            t_input = input(q_str).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            max_c = max(250, target_val * 15)
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, timeout=3.0)
        elif choice == "2":
            q_str = f"{Fore.CYAN}{'Target proxy SOCKS5 hidup [default: 15]: ' if CURRENT_LANG == 'ID' else 'Target alive SOCKS5 count [default: 15]: '}{Style.RESET_ALL}"
            t_input = input(q_str).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            max_c = max(250, target_val * 15)
            run_harvester(protocols=["socks5"], max_check=max_c, target_alive=target_val, timeout=3.0)
        elif choice == "3":
            q_str = f"{Fore.CYAN}{'Target proxy HTTP hidup [default: 15]: ' if CURRENT_LANG == 'ID' else 'Target alive HTTP count [default: 15]: '}{Style.RESET_ALL}"
            t_input = input(q_str).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            max_c = max(250, target_val * 15)
            run_harvester(protocols=["http"], max_check=max_c, target_alive=target_val, timeout=3.0)
        elif choice == "4":
            cc_prompt = f"{Fore.CYAN}{'Masukkan 2 huruf kode negara (contoh: ID, SG, US) [default: ID]: ' if CURRENT_LANG == 'ID' else 'Enter 2-letter Country Code (e.g. ID, SG, US) [default: ID]: '}{Style.RESET_ALL}"
            cc = input(cc_prompt).strip() or "ID"
            t_prompt = f"{Fore.CYAN}{'Target proxy hidup [default: 5]: ' if CURRENT_LANG == 'ID' else 'Target alive count [default: 5]: '}{Style.RESET_ALL}"
            t_input = input(t_prompt).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 5
            max_c = max(350, target_val * 35)
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, country=cc, timeout=3.5)
        elif choice == "5":
            q_str = f"{Fore.CYAN}{'Target proxy Elite (Anti Bocor) [default: 15]: ' if CURRENT_LANG == 'ID' else 'Target alive Elite proxies count [default: 15]: '}{Style.RESET_ALL}"
            t_input = input(q_str).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            max_c = max(350, target_val * 20)
            print(f"\n{Fore.CYAN}{'🛡️ Menyaring khusus proxy Elite (High Anonymity)...' if CURRENT_LANG == 'ID' else '🛡️ Filtering for Elite (High Anonymous) proxies only...'}{Style.RESET_ALL}")
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, anonymity="elite", timeout=3.0)
        elif choice == "6":
            u_prompt = f"{Fore.CYAN}{'Masukkan URL web target [default: https://google.com]: ' if CURRENT_LANG == 'ID' else 'Enter target URL to test against [default: https://google.com]: '}{Style.RESET_ALL}"
            t_url = input(u_prompt).strip() or "https://google.com"
            t_prompt = f"{Fore.CYAN}{'Target proxy lolos [default: 10]: ' if CURRENT_LANG == 'ID' else 'Target alive count [default: 10]: '}{Style.RESET_ALL}"
            t_input = input(t_prompt).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 10
            max_c = max(400, target_val * 25)
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, target_url=t_url, timeout=3.5)
        elif choice == "7":
            port_prompt = f"{Fore.CYAN}{'Port lokal untuk Rotating Gateway & API [default: 8888]: ' if CURRENT_LANG == 'ID' else 'Enter local port for Rotating Gateway & API [default: 8888]: '}{Style.RESET_ALL}"
            port_input = input(port_prompt).strip()
            port_val = int(port_input) if port_input.isdigit() else 8888
            t_prompt = f"{Fore.CYAN}{'Jumlah proxy hidup di pool [default: 15]: ' if CURRENT_LANG == 'ID' else 'Target alive pool size [default: 15]: '}{Style.RESET_ALL}"
            t_input = input(t_prompt).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            max_c = max(300, target_val * 15)
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, timeout=3.0, serve_port=port_val)
        elif choice == "8":
            t_prompt = f"{Fore.CYAN}{'Target proxy per putaran [default: 20]: ' if CURRENT_LANG == 'ID' else 'Target alive proxies per sweep [default: 20]: '}{Style.RESET_ALL}"
            t_input = input(t_prompt).strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 20
            l_prompt = f"{Fore.CYAN}{'Interval putaran (dalam menit) [default: 20]: ' if CURRENT_LANG == 'ID' else 'Enter refresh interval in minutes [default: 20]: '}{Style.RESET_ALL}"
            loop_str = input(l_prompt).strip()
            loop_min = int(loop_str) if loop_str.isdigit() and int(loop_str) > 0 else 20
            max_c = max(300, target_val * 15)
            print(f"\n{Fore.MAGENTA}{'🔄 Auto-refresh aktif: Panen' if CURRENT_LANG == 'ID' else '🔄 Auto-refresh active: Target'} {target_val} proxies {'setiap' if CURRENT_LANG == 'ID' else 'every'} {loop_min} {'menit. Tekan Ctrl+C untuk kembali.' if CURRENT_LANG == 'ID' else 'minutes. Press Ctrl+C to return.'}{Style.RESET_ALL}")
            while True:
                try:
                    run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, timeout=3.0)
                    print(f"{Fore.LIGHTBLACK_EX}{'Tidur selama' if CURRENT_LANG == 'ID' else 'Sleeping for'} {loop_min} {'menit sebelum panen berikutnya...' if CURRENT_LANG == 'ID' else 'minutes before next cycle...'}{Style.RESET_ALL}")
                    time.sleep(loop_min * 60)
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}{'Loop dihentikan.' if CURRENT_LANG == 'ID' else 'Loop stopped.'}{Style.RESET_ALL}")
                    break
        elif choice == "9":
            possible_path = "D:/FREELANCE/9router-mibp-version/data/db/data.sqlite"
            custom_path = input(f"{Fore.CYAN}{'Path ke file data.sqlite 9Router [Enter untuk deteksi otomatis]: ' if CURRENT_LANG == 'ID' else 'Enter 9Router data.sqlite path [press Enter for auto-detect]: '}{Style.RESET_ALL}").strip()
            db_target = custom_path if custom_path else (possible_path if os.path.exists(possible_path) else None)
            if db_target:
                run_harvester(protocols=["http", "socks4", "socks5"], max_check=250, target_alive=15, sync_9router=db_target)
            else:
                print(f"{Fore.RED}{'Database 9Router tidak ditemukan.' if CURRENT_LANG == 'ID' else '9Router database not found.'}{Style.RESET_ALL}")
        elif choice.lower() in ("s", "saved"):
            view_saved_results()
        elif choice == "0" or choice.lower() == "q":
            goodbye_msg = "💀 Pelayanan selesai. Terima kasih sudah mampir! 👋" if CURRENT_LANG == "ID" else "💀 Aight imma head out — session terminated. Goodbye! 👋"
            print(f"\n{Fore.YELLOW}{goodbye_msg}{Style.RESET_ALL}\n")
            break
        else:
            invalid_msg = "Pilihan tidak valid. Silakan pilih P, 0-9, S, atau L." if CURRENT_LANG == "ID" else "Invalid choice. Please select P, 0-9, S, or L."
            print(f"{Fore.RED}{invalid_msg}{Style.RESET_ALL}")

        try:
            pause_msg = "[Tekan Enter untuk kembali ke menu...]" if CURRENT_LANG == "ID" else "[Press Enter to return to menu...]"
            input(f"\n{Fore.LIGHTBLACK_EX}{pause_msg}{Style.RESET_ALL}")
        except (KeyboardInterrupt, EOFError):
            break

def main():
    if len(sys.argv) == 1:
        show_interactive_menu()
        return

    parser = argparse.ArgumentParser(description="OmniProxy Harvester - High-Speed Multi-Protocol Proxy Harvester")
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
    parser.add_argument("--sync-9router", type=str, default=None, help="Path to 9Router data.sqlite for direct database sync")

    args = parser.parse_args()

    print(BANNER)
    proto_list = [args.protocol] if args.protocol != "all" else ["http", "socks4", "socks5"]

    # Check for automatic 9Router discovery if requested
    router_db = args.sync_9router
    if router_db == "auto":
        possible_path = "D:/FREELANCE/9router-mibp-version/data/db/data.sqlite"
        if os.path.exists(possible_path):
            router_db = possible_path

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
