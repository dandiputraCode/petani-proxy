"""
core/updater.py - Auto-Updater & Version Patch Notification System for PetaniProxy.
Inspired by 9Router's seamless in-app updater.
"""
import os
import sys
import json
import subprocess
import requests
from typing import Dict, Any, Optional, Tuple, List

# Force UTF-8 on Windows
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from colorama import Fore, Style
except ImportError:
    class DummyColor:
        def __getattr__(self, name):
            return ""
    Fore = Style = DummyColor()

GITHUB_REPO = "itzluthfi/petani-proxy"
REMOTE_VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/version.json"

def get_base_dir() -> str:
    """Get the root directory of petani-proxy."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_local_version_info() -> Dict[str, Any]:
    """Read local version.json metadata."""
    version_file = os.path.join(get_base_dir(), "version.json")
    if os.path.exists(version_file):
        try:
            with open(version_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": "1.0.0",
        "release_date": "2026-09-14",
        "title": "🌾 PetaniProxy v1.0.0",
        "announcement": "Rilis perdana PetaniProxy v1.0",
        "changelog": []
    }

def parse_version_tuple(v: str) -> Tuple[int, ...]:
    """Parse version string like '1.0.0' or 'v1.2.3' into a comparable tuple (1, 2, 3)."""
    clean_v = v.lower().strip().lstrip("v")
    parts = []
    for part in clean_v.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)

def check_for_updates(timeout: float = 2.5) -> Dict[str, Any]:
    """
    Check if a newer version is available on GitHub.
    Returns dictionary with update details, announcement, and changelog.
    """
    local_info = get_local_version_info()
    local_ver_str = local_info.get("version", "1.0.0")
    local_tuple = parse_version_tuple(local_ver_str)

    result = {
        "has_update": False,
        "current_version": local_ver_str,
        "remote_version": local_ver_str,
        "title": local_info.get("title", "PetaniProxy"),
        "announcement": local_info.get("announcement", ""),
        "release_date": local_info.get("release_date", "-"),
        "changelog": local_info.get("changelog", []),
        "error": None
    }

    try:
        # Fetch latest version.json from raw GitHub
        resp = requests.get(REMOTE_VERSION_URL, timeout=timeout)
        if resp.status_code == 200:
            remote_data = resp.json()
            remote_ver_str = remote_data.get("version", local_ver_str)
            remote_tuple = parse_version_tuple(remote_ver_str)

            result["remote_version"] = remote_ver_str
            result["title"] = remote_data.get("title", f"PetaniProxy v{remote_ver_str}")
            result["announcement"] = remote_data.get("announcement", "")
            result["release_date"] = remote_data.get("release_date", "-")
            result["changelog"] = remote_data.get("changelog", [])

            if remote_tuple > local_tuple:
                result["has_update"] = True
                return result

        # Also check git commit distance if in a git repository
        git_dir = os.path.join(get_base_dir(), ".git")
        if os.path.exists(git_dir):
            try:
                fetch_cmd = subprocess.run(
                    ["git", "fetch", "origin", "master", "--quiet"],
                    cwd=get_base_dir(),
                    capture_output=True,
                    text=True,
                    timeout=3.0
                )
                if fetch_cmd.returncode == 0:
                    status_cmd = subprocess.run(
                        ["git", "rev-list", "--count", "HEAD..origin/master"],
                        cwd=get_base_dir(),
                        capture_output=True,
                        text=True,
                        timeout=2.0
                    )
                    ahead_count = int(status_cmd.stdout.strip() or 0)
                    if ahead_count > 0:
                        result["has_update"] = True
                        if not result["changelog"]:
                            log_cmd = subprocess.run(
                                ["git", "log", "-n", str(min(ahead_count, 5)), "--pretty=format:%s", "origin/master"],
                                cwd=get_base_dir(),
                                capture_output=True,
                                text=True,
                                timeout=2.0
                            )
                            result["changelog"] = [c.strip() for c in log_cmd.stdout.strip().split("\n") if c.strip()]
            except Exception:
                pass

    except Exception as e:
        result["error"] = str(e)

    return result

def render_update_banner(update_info: Dict[str, Any], lang: str = "ID") -> str:
    """Render a compact terminal banner displaying update notification and announcement."""
    curr = update_info.get("current_version", "1.0.0")
    remote = update_info.get("remote_version", "1.0.0")
    title = update_info.get("title", f"PetaniProxy v{remote}")
    announcement = update_info.get("announcement", "")
    changelog = update_info.get("changelog", [])

    lines = []
    lines.append(f"{Fore.YELLOW}┌────────────────────────────────────────────────────────────────────────┐")
    if lang == "ID":
        lines.append(f"│ {Fore.WHITE}{Style.BRIGHT}🚀 UPDATE TERSEDIA! {Fore.GREEN}v{remote}{Fore.WHITE} (Versi Terpasang: {Fore.YELLOW}v{curr}{Fore.WHITE}){Fore.YELLOW}                       │")
        if announcement:
            ann_clean = announcement[:60]
            lines.append(f"│ 📢 {Fore.CYAN}{ann_clean:<67}{Fore.YELLOW}│")
        lines.append(f"├────────────────────────────────────────────────────────────────────────┤")
        lines.append(f"│ {Fore.MAGENTA}📝 Rincian Pembaruan & Fitur Baru:{Fore.YELLOW}                                     │")
    else:
        lines.append(f"│ {Fore.WHITE}{Style.BRIGHT}🚀 NEW UPDATE AVAILABLE! {Fore.GREEN}v{remote}{Fore.WHITE} (Current: {Fore.YELLOW}v{curr}{Fore.WHITE}){Fore.YELLOW}                       │")
        if announcement:
            ann_clean = announcement[:60]
            lines.append(f"│ 📢 {Fore.CYAN}{ann_clean:<67}{Fore.YELLOW}│")
        lines.append(f"├────────────────────────────────────────────────────────────────────────┤")
        lines.append(f"│ {Fore.MAGENTA}📝 Patch Notes & What's New:{Fore.YELLOW}                                           │")

    if changelog:
        for item in changelog[:4]:
            item_clean = item.strip()
            if len(item_clean) > 64:
                item_clean = item_clean[:61] + "..."
            lines.append(f"│   {Fore.WHITE}• {item_clean:<65}{Fore.YELLOW}│")
    else:
        hint = "Peningkatan performa & perbaikan bug." if lang == "ID" else "Performance improvements & bug fixes."
        lines.append(f"│   {Fore.WHITE}• {hint:<65}{Fore.YELLOW}│")

    lines.append(f"├────────────────────────────────────────────────────────────────────────┤")
    cta = "👉 Tekan [U] di menu untuk update otomatis dalam 1 klik! ✨" if lang == "ID" else "👉 Press [U] in menu for seamless 1-click update! ✨"
    lines.append(f"│ {Fore.GREEN}{Style.BRIGHT}{cta:<70}{Fore.YELLOW} │")
    lines.append(f"└────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")

    return "\n".join(lines)

def show_full_announcement(info: Dict[str, Any], lang: str = "ID"):
    """Display full changelog, announcement and release notes modal in terminal."""
    ver = info.get("version") or info.get("remote_version") or "1.0.0"
    date = info.get("release_date", "-")
    title = info.get("title", f"PetaniProxy v{ver}")
    ann = info.get("announcement", "")
    changelog = info.get("changelog", [])

    print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{Style.BRIGHT}📢 INFORMASI RILIS & PENGUMUMAN UPDATE (PETANIPROXY v{ver}){Style.RESET_ALL}")
    print(f"  • Tanggal Rilis : {Fore.YELLOW}{date}{Style.RESET_ALL}")
    print(f"  • Judul Rilis   : {Fore.GREEN}{title}{Style.RESET_ALL}")
    if ann:
        print(f"  • Highlight     : {Fore.CYAN}{ann}{Style.RESET_ALL}")
    print(f"\n{Fore.MAGENTA}DAFTAR LENGKAP FITUR BARU & PATCH NOTES:{Style.RESET_ALL}")
    for idx, item in enumerate(changelog, 1):
        print(f"  {Fore.YELLOW}{idx:>2}.{Fore.WHITE} {item}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")

def perform_update(restart: bool = True, lang: str = "ID") -> bool:
    """
    Execute git pull origin master, display announcement, and update dependencies.
    """
    base_dir = get_base_dir()
    print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}{'🚀 MEMULAI PROSES UPDATE PETANIPROXY...' if lang == 'ID' else '🚀 LAUNCHING PETANIPROXY AUTO-UPDATE...'}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}{'Menghubungkan ke repositori pusat (github.com/itzluthfi/petani-proxy)...' if lang == 'ID' else 'Connecting to upstream repo (github.com/itzluthfi/petani-proxy)...'}{Style.RESET_ALL}\n")

    # Step 1: Git pull
    print(f"  {Fore.YELLOW}[1/3]{Fore.WHITE} {'Mengambil commit & patch terbaru via Git...' if lang == 'ID' else 'Pulling latest commits & patches via Git...'}{Style.RESET_ALL}")
    try:
        pull = subprocess.run(["git", "pull", "origin", "master"], cwd=base_dir, capture_output=True, text=True)
        if pull.returncode == 0:
            print(f"       {Fore.GREEN}✓ Git Pull Sukses:{Style.RESET_ALL} {pull.stdout.strip().splitlines()[0] if pull.stdout else 'Up to date'}")
        else:
            print(f"       {Fore.RED}⚠️ Git Pull Gagal:{Style.RESET_ALL} {pull.stderr.strip()}")
            print(f"       {Fore.YELLOW}Mencoba fetch & reset hard ke origin/master...{Style.RESET_ALL}")
            subprocess.run(["git", "fetch", "origin", "master"], cwd=base_dir)
            subprocess.run(["git", "reset", "--hard", "origin/master"], cwd=base_dir)
    except Exception as e:
        print(f"       {Fore.RED}❌ Gagal menjalankan git: {e}{Style.RESET_ALL}")
        return False

    # Step 2: Install / Update requirements
    print(f"\n  {Fore.YELLOW}[2/3]{Fore.WHITE} {'Memeriksa pembaruan dependensi paket (requirements.txt)...' if lang == 'ID' else 'Checking dependency updates (requirements.txt)...'}{Style.RESET_ALL}")
    req_file = os.path.join(base_dir, "requirements.txt")
    if os.path.exists(req_file):
        try:
            pip_res = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"], cwd=base_dir)
            if pip_res.returncode == 0:
                print(f"       {Fore.GREEN}✓ Semua dependensi up-to-date!{Style.RESET_ALL}")
            else:
                print(f"       {Fore.YELLOW}⚠️ Pip install selesai dengan catatan.{Style.RESET_ALL}")
        except Exception as e:
            print(f"       {Fore.RED}⚠️ Gagal mengupdate dependensi: {e}{Style.RESET_ALL}")

    # Step 3: Show new version & announcement
    print(f"\n  {Fore.YELLOW}[3/3]{Fore.WHITE} {'Membaca pengumuman & rincian versi baru...' if lang == 'ID' else 'Reading updated version announcement...'}{Style.RESET_ALL}")
    new_info = get_local_version_info()
    new_ver = new_info.get("version", "1.0.0")

    show_full_announcement(new_info, lang=lang)

    print(f"{Fore.GREEN}{Style.BRIGHT}{'🎉 PETANIPROXY SUKSES DIPERBARUI KE v' + new_ver + '!' if lang == 'ID' else '🎉 PETANIPROXY SUCCESSFULLY UPDATED TO v' + new_ver + '!'}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Semua fitur dan patch baru siap digunakan! 🌾🚜{Style.RESET_ALL}\n")

    if restart:
        try:
            prompt_restart = f"{Fore.YELLOW}{'Ingin me-restart PetaniProxy sekarang? [Y/n]: ' if lang == 'ID' else 'Restart PetaniProxy now? [Y/n]: '}{Style.RESET_ALL}"
            ans = input(prompt_restart).strip().lower()
            if ans in ("", "y", "yes"):
                print(f"{Fore.GREEN}{'Memuat ulang program...' if lang == 'ID' else 'Restarting program...'}{Style.RESET_ALL}\n")
                python = sys.executable
                os.execv(python, [python] + sys.argv)
        except Exception:
            pass

    return True
