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

def show_presets_menu():
    while True:
        print(BANNER)
        p_box = f"""{Fore.CYAN}┌────────────────────────────────────────────────────────────────────────┐
│                   {Fore.WHITE}{Style.BRIGHT}🎯 ONE-CLICK USE-CASE PRESETS MENU{Fore.CYAN}                   │
│         {Fore.LIGHTBLACK_EX}Pre-tuned production pipelines for common dev tasks{Fore.CYAN}            │
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.GREEN}[1]{Fore.WHITE} 🤖 AI & LLM Bot Rotator  {Fore.LIGHTBLACK_EX}Ultra-low latency (<1.5s), runs on 8888  {Fore.CYAN}│
│                               {Fore.LIGHTBLACK_EX}& auto-syncs to 9Router SQLite pool      {Fore.CYAN}│
│  {Fore.GREEN}[2]{Fore.WHITE} 🕷 Mass Web Scraper      {Fore.LIGHTBLACK_EX}Harvests 30+ strict Elite nodes & starts {Fore.CYAN}│
│                               {Fore.LIGHTBLACK_EX}failover proxy server for Scrapy/Selenium{Fore.CYAN}│
│  {Fore.GREEN}[3]{Fore.WHITE} 🌍 SEO & Geo-Target      {Fore.LIGHTBLACK_EX}Verifies region proxies against Google   {Fore.CYAN}│
│                               {Fore.LIGHTBLACK_EX}for accurate SERP & ad auditing          {Fore.CYAN}│
│  {Fore.GREEN}[4]{Fore.WHITE} 🛡 Privacy & Unblocker   {Fore.LIGHTBLACK_EX}Fast regional nodes for unblocking       {Fore.CYAN}│
│                               {Fore.LIGHTBLACK_EX}foreign developer sites without paid VPN {Fore.CYAN}│
│  {Fore.RED}[0]{Fore.WHITE} 🔙 Back to Main Menu     {Fore.LIGHTBLACK_EX}Return to primary selection              {Fore.CYAN}│
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.LIGHTBLACK_EX}Maintainer: {Fore.YELLOW}@itzluthfi{Fore.LIGHTBLACK_EX}          Repository: {Fore.WHITE}github.com/itzluthfi{Fore.CYAN}       │
└────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}"""
        print(p_box)
        try:
            choice = input(f"{Fore.YELLOW}Select preset [1-4, 0=Back]: {Style.RESET_ALL}").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if choice == "1":
            print(f"\n{Fore.GREEN}🤖 Launching AI & LLM Bot Rotator Preset...{Style.RESET_ALL}")
            possible_path = "D:/FREELANCE/9router-mibp-version/data/db/data.sqlite"
            db = possible_path if os.path.exists(possible_path) else None
            run_harvester(protocols=["http", "socks5"], max_check=350, target_alive=20, timeout=2.5, serve_port=8888, sync_9router=db)
        elif choice == "2":
            print(f"\n{Fore.GREEN}🕷️ Launching Mass Web Scraper Preset...{Style.RESET_ALL}")
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=500, target_alive=30, anonymity="elite", timeout=3.0, serve_port=8888)
        elif choice == "3":
            cc = input(f"{Fore.CYAN}Enter target country for SEO audit [default: US]: {Style.RESET_ALL}").strip() or "US"
            print(f"\n{Fore.GREEN}🌍 Launching SEO & Geo-Target Preset for [{cc}]...{Style.RESET_ALL}")
            run_harvester(protocols=["http", "socks5"], max_check=400, target_alive=10, country=cc, target_url="https://google.com", timeout=3.5)
        elif choice == "4":
            print(f"\n{Fore.GREEN}🛡️ Launching Browser Privacy & Unblocker Preset...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Tip: After server starts, configure your browser proxy to 127.0.0.1:8888!{Style.RESET_ALL}")
            run_harvester(protocols=["http", "socks5"], max_check=300, target_alive=10, country="SG", timeout=2.5, serve_port=8888)
        elif choice in ("0", "b", "back", "q"):
            break
        else:
            print(f"{Fore.RED}Pilihan preset tidak valid.{Style.RESET_ALL}")

        try:
            input(f"\n{Fore.LIGHTBLACK_EX}[Press Enter to return to Presets menu...]{Style.RESET_ALL}")
        except (KeyboardInterrupt, EOFError):
            break

def show_interactive_menu():
    while True:
        print(BANNER)
        menu_box = f"""{Fore.CYAN}┌────────────────────────────────────────────────────────────────────────┐
│                        {Fore.WHITE}{Style.BRIGHT}OMNIPROXY HARVESTER MENU{Fore.CYAN}                        │
│                 {Fore.LIGHTBLACK_EX}High-Speed Multi-Protocol Scraper & Validator{Fore.CYAN}          │
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.MAGENTA}[P]{Fore.WHITE} 🎯 Use-Case Presets   {Fore.LIGHTBLACK_EX}One-Click Presets for AI, Scraper, SEO, etc {Fore.CYAN}│
│  {Fore.GREEN}[1]{Fore.WHITE} ⚡ Quick Harvest         {Fore.LIGHTBLACK_EX}Find fast proxies (Customizable Target)  {Fore.CYAN}│
│  {Fore.GREEN}[2]{Fore.WHITE} 🔒 SOCKS5 Only           {Fore.LIGHTBLACK_EX}Harvest high-speed SOCKS5 proxies        {Fore.CYAN}│
│  {Fore.GREEN}[3]{Fore.WHITE} 🌐 HTTP / HTTPS Only     {Fore.LIGHTBLACK_EX}Harvest web-browsing HTTP nodes          {Fore.CYAN}│
│  {Fore.GREEN}[4]{Fore.WHITE} 🌍 Target by Country     {Fore.LIGHTBLACK_EX}Filter by ISO Code (ID, SG, US, DE, JP) {Fore.CYAN}│
│  {Fore.GREEN}[5]{Fore.WHITE} 🛡 Elite Proxies Only    {Fore.LIGHTBLACK_EX}Strict High-Anonymity nodes (No Leaks)   {Fore.CYAN}│
│  {Fore.GREEN}[6]{Fore.WHITE} 🎯 Target-Specific Test  {Fore.LIGHTBLACK_EX}Test against custom URL (Google/Shop)    {Fore.CYAN}│
│  {Fore.GREEN}[7]{Fore.WHITE} 🚀 Local Rotating Server {Fore.LIGHTBLACK_EX}Start localhost:8888 Proxy & REST API    {Fore.CYAN}│
│  {Fore.GREEN}[8]{Fore.WHITE} 🔄 Auto-Refresh Daemon   {Fore.LIGHTBLACK_EX}Loop run continuously every N minutes    {Fore.CYAN}│
│  {Fore.GREEN}[9]{Fore.WHITE} 🔌 Sync to 9Router       {Fore.LIGHTBLACK_EX}Inject live proxies into 9Router SQLite  {Fore.CYAN}│
│  {Fore.GREEN}[S]{Fore.WHITE} 📂 View Saved Output     {Fore.LIGHTBLACK_EX}Inspect last results in output/ directory{Fore.CYAN}│
│  {Fore.RED}[0]{Fore.WHITE} ❌ Exit Program          {Fore.LIGHTBLACK_EX}Close terminal session                   {Fore.CYAN}│
├────────────────────────────────────────────────────────────────────────┤
│  {Fore.LIGHTBLACK_EX}Maintainer: {Fore.YELLOW}@itzluthfi{Fore.LIGHTBLACK_EX}          Repository: {Fore.WHITE}github.com/itzluthfi{Fore.CYAN}       │
└────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}"""
        print(menu_box)
        try:
            choice = input(f"{Fore.YELLOW}Select option [P, 0-9, S] (Default: 1): {Style.RESET_ALL}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break

        if choice.lower() == "p":
            show_presets_menu()
            continue

        if choice == "" or choice == "1":
            t_input = input(f"{Fore.CYAN}Target alive proxies count [default: 15]: {Style.RESET_ALL}").strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            max_c = max(250, target_val * 15)
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, timeout=3.0)
        elif choice == "2":
            t_input = input(f"{Fore.CYAN}Target alive SOCKS5 proxies count [default: 15]: {Style.RESET_ALL}").strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            max_c = max(250, target_val * 15)
            run_harvester(protocols=["socks5"], max_check=max_c, target_alive=target_val, timeout=3.0)
        elif choice == "3":
            t_input = input(f"{Fore.CYAN}Target alive HTTP proxies count [default: 15]: {Style.RESET_ALL}").strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            max_c = max(250, target_val * 15)
            run_harvester(protocols=["http"], max_check=max_c, target_alive=target_val, timeout=3.0)
        elif choice == "4":
            cc = input(f"{Fore.CYAN}Enter 2-letter Country Code (e.g. ID, SG, US, DE, JP) [default: ID]: {Style.RESET_ALL}").strip() or "ID"
            t_input = input(f"{Fore.CYAN}Target alive count [default: 5]: {Style.RESET_ALL}").strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 5
            max_c = max(350, target_val * 35)
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, country=cc, timeout=3.5)
        elif choice == "5":
            t_input = input(f"{Fore.CYAN}Target alive Elite proxies count [default: 15]: {Style.RESET_ALL}").strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            max_c = max(350, target_val * 20)
            print(f"\n{Fore.CYAN}🛡️ Filtering for Elite (High Anonymous) proxies only...{Style.RESET_ALL}")
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, anonymity="elite", timeout=3.0)
        elif choice == "6":
            t_url = input(f"{Fore.CYAN}Enter target URL to test against [default: https://google.com]: {Style.RESET_ALL}").strip() or "https://google.com"
            t_input = input(f"{Fore.CYAN}Target alive count [default: 10]: {Style.RESET_ALL}").strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 10
            max_c = max(400, target_val * 25)
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, target_url=t_url, timeout=3.5)
        elif choice == "7":
            port_input = input(f"{Fore.CYAN}Enter local port for Rotating Gateway & API [default: 8888]: {Style.RESET_ALL}").strip()
            port_val = int(port_input) if port_input.isdigit() else 8888
            t_input = input(f"{Fore.CYAN}Target alive proxies pool size [default: 15]: {Style.RESET_ALL}").strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 15
            max_c = max(300, target_val * 15)
            run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, timeout=3.0, serve_port=port_val)
        elif choice == "8":
            t_input = input(f"{Fore.CYAN}Target alive proxies count per sweep [default: 20]: {Style.RESET_ALL}").strip()
            target_val = int(t_input) if t_input.isdigit() and int(t_input) > 0 else 20
            loop_str = input(f"{Fore.CYAN}Enter refresh interval in minutes [default: 20]: {Style.RESET_ALL}").strip()
            loop_min = int(loop_str) if loop_str.isdigit() and int(loop_str) > 0 else 20
            max_c = max(300, target_val * 15)
            print(f"\n{Fore.MAGENTA}🔄 Auto-refresh active: Target {target_val} proxies every {loop_min} minutes. Press Ctrl+C to return to menu.{Style.RESET_ALL}")
            while True:
                try:
                    run_harvester(protocols=["http", "socks4", "socks5"], max_check=max_c, target_alive=target_val, timeout=3.0)
                    print(f"{Fore.LIGHTBLACK_EX}Sleeping for {loop_min} minutes before next cycle...{Style.RESET_ALL}")
                    time.sleep(loop_min * 60)
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Loop stopped.{Style.RESET_ALL}")
                    break
        elif choice == "9":
            possible_path = "D:/FREELANCE/9router-mibp-version/data/db/data.sqlite"
            custom_path = input(f"{Fore.CYAN}Enter 9Router data.sqlite path [press Enter for auto-detect]: {Style.RESET_ALL}").strip()
            db_target = custom_path if custom_path else (possible_path if os.path.exists(possible_path) else None)
            if db_target:
                run_harvester(protocols=["http", "socks4", "socks5"], max_check=250, target_alive=15, sync_9router=db_target)
            else:
                print(f"{Fore.RED}Database 9Router tidak ditemukan.{Style.RESET_ALL}")
        elif choice.lower() in ("s", "saved"):
            view_saved_results()
        elif choice == "0" or choice.lower() == "q":
            print(f"\n{Fore.YELLOW}Terima kasih telah menggunakan OmniProxy Harvester! 👋{Style.RESET_ALL}\n")
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid. Silakan pilih 0-9 atau S.{Style.RESET_ALL}")

        try:
            input(f"\n{Fore.LIGHTBLACK_EX}[Press Enter to return to menu...]{Style.RESET_ALL}")
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
