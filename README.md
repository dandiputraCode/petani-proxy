<div align="center">

# 🌐 OmniProxy Harvester
### High-Speed Multi-Protocol Open-Source Proxy Harvester, Checker & GeoIP Enricher

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-brightgreen.svg)](https://python.org)
[![Protocols](https://img.shields.io/badge/Protocols-HTTP%20%7C%20HTTPS%20%7C%20SOCKS4%20%7C%20SOCKS5-orange.svg)](#features)
[![GeoIP Detection](https://img.shields.io/badge/Enrichment-GeoIP%20%26%20ISP-purple.svg)](#output-formats)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-green.svg)](https://github.com/)

**OmniProxy Harvester** scrapes, deduplicates, and benchmarks **100,000+ public proxy candidates in seconds** from 30+ open-source feeds across **HTTP, HTTPS, SOCKS4, and SOCKS5**. It filters out dead nodes in parallel, benchmarks real millisecond latencies, enriches live proxies with country and ISP information, and exports clean lists in **TXT, JSON, and CSV**.

</div>

---

```
  ██████╗ ███╗   ███╗███╗   ██╗██╗██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
 ██╔═══██╗████╗ ████║████╗  ██║██║██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
 ██║   ██║██╔████╔██║██╔██╗ ██║██║██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
 ██║   ██║██║╚██╔╝██║██║╚██╗██║██║██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
 ╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
```

---

## 🚀 Key Features

- ⚡ **Astronomical Scale**: Scrapes **115,000+ candidates** from 30+ raw GitHub & API feeds in under **3 seconds**.
- 🛡️ **Multi-Protocol Support**: Full native support for **HTTP**, **HTTPS**, **SOCKS4**, and **SOCKS5**.
- ⏱️ **Real-Time Latency Testing**: Accurately tests live HTTPS handshake latency in milliseconds against `https://api.ipify.org`.
- 🌍 **GeoIP & ISP Enrichment**: Automatically resolves Country (e.g. `[US] United States`, `[SG] Singapore`, `[ID] Indonesia`), City, and ISP for all alive proxies via non-rate-limited batch queries.
- 🎯 **Smart Early Stopping**: Stops immediately once your `--target` alive count is satisfied, preventing wasted bandwidth.
- 📦 **Multi-Format Exporters**:
  - `live_all.txt` & `live_urls.txt` (`protocol://ip:port`)
  - Protocol-separated lists: `live_http.txt`, `live_socks4.txt`, `live_socks5.txt`
  - `proxies.json` with full metadata
  - `proxies.csv` spreadsheet
- 🤖 **GitHub Actions CI/CD Ready**: Includes a turnkey `.github/workflows/auto_harvest.yml` workflow that auto-scrapes every 6 hours and commits fresh proxies to your repository.
- 🔄 **Direct 9Router & AI Proxy Pool Sync**: Optional `--sync-9router` flag to directly inject live proxies into 9Router LLM router databases.

---

## 📡 Transparency: Where Do The Proxies Come From?

OmniProxy Harvester aggregates only **public, open-source proxy feeds** that are actively maintained by community security researchers and open-data projects. All sources are defined in [`config/sources.json`](config/sources.json):

| Category | Source Provider / Repository | Protocol | Type |
| :--- | :--- | :--- | :--- |
| **ProxyScrape API** | `api.proxyscrape.com` | HTTP, SOCKS4, SOCKS5 | Public Elite / Transparent API |
| **TheSpeedX** | `TheSpeedX/PROXY-List` | HTTP, SOCKS4, SOCKS5 | GitHub Raw Feed |
| **monosans** | `monosans/proxy-list` | HTTP, SOCKS4, SOCKS5 | GitHub Raw Feed |
| **hookzof** | `hookzof/socks5_list` | SOCKS5 | High-Quality SOCKS5 Feed |
| **clarketm** | `clarketm/proxy-list` | HTTP / HTTPS | GitHub Raw Feed |
| **roosterkid** | `roosterkid/openproxylist` | HTTPS, SOCKS4, SOCKS5 | GitHub Raw Feed |
| **sunny9577** | `sunny9577/proxy-scraper` | HTTP / HTTPS | GitHub Raw Feed |
| **ShiftyTR** | `ShiftyTR/Proxy-List` | HTTP, HTTPS, SOCKS4, SOCKS5 | GitHub Raw Feed |
| **B4RC0DE-TM**| `B4RC0DE-TM/proxy-list` | HTTP, SOCKS4, SOCKS5 | GitHub Raw Feed |
| **zevtyardt** | `zevtyardt/proxy-list` | HTTP, SOCKS4, SOCKS5 | GitHub Raw Feed |
| **mertguvencli**| `mertguvencli/http-proxy-list` | HTTP | GitHub Raw Feed |
| **hendrikbgr** | `hendrikbgr/Free-Proxy-Repo` | HTTP | GitHub Raw Feed |
| **RX007** | `RX007/Proxy-List` | HTTP | GitHub Raw Feed |
| **almroot** | `almroot/proxylist` | HTTP | GitHub Raw Feed |
| **manuGMG** | `manuGMG/proxy-365` | SOCKS5 | GitHub Raw Feed |

> 💡 *Want to add your own feeds? Simply add raw URLs to `config/sources.json`!*

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/omni-proxy-harvester.git
cd omni-proxy-harvester

# 2. Install dependencies
pip install -r requirements.txt
```

---

## 💻 Usage & CLI Examples

### 1. Basic Fast Run (All Protocols)
Find 15 alive proxies with default 3.0s timeout:
```bash
python main.py
```

### 2. SOCKS5 Only
Harvest and test only high-performance SOCKS5 nodes:
```bash
python main.py --protocol socks5 --target 25 --timeout 2.5
```

### 3. Filter by Specific Country
Only collect proxies residing in a specific country (e.g. `US`, `SG`, `ID`, `DE`):
```bash
python main.py --country SG --target 10
```

### 4. High-Concurrency Deep Sweep
Test 1,000 candidates with 80 parallel workers to gather 50 fast proxies:
```bash
python main.py --max 1000 --target 50 --workers 80 --timeout 2.0
```

### 5. Automated Background Daemon (Auto-Refresh)
Run continuously and refresh live proxy lists every 30 minutes:
```bash
python main.py --loop 30 --target 30
```

### 6. Sync Directly to 9Router Proxy Pool
Inject verified live proxies directly into your 9Router SQLite database:
```bash
python main.py --sync-9router "path/to/9router/data.sqlite"
```

---

## ⚙️ Command-Line Arguments Reference

| Argument | Shorthand | Default | Description |
| :--- | :--- | :--- | :--- |
| `--protocol` | `-p` | `all` | Protocols to scrape: `all`, `http`, `socks4`, or `socks5`. |
| `--max` | `-m` | `250` | Maximum candidate proxies to test from pool. |
| `--target` | `-t` | `15` | Stop testing once this many alive proxies are verified. |
| `--timeout` | | `3.0` | Connection timeout in seconds. Lower = faster proxies. |
| `--workers` | `-w` | `50` | Concurrency worker threads for validation. |
| `--country` | `-c` | `None` | Filter by 2-letter ISO Country Code (e.g. `US`, `SG`, `ID`). |
| `--loop` | `-l` | `0` | Repeat harvest every `N` minutes (0 = single run). |
| `--output` | `-o` | `output/` | Destination folder for exported files. |
| `--sync-9router` | | `None` | Path to 9Router SQLite database to update proxy pools. |

---

## 📂 Output Formats

All verified proxies are exported into the `output/` folder:

### 1. `output/proxies.json`
Structured JSON with complete network, latency, and GeoIP metadata:
```json
{
  "generated_at": "2026-09-13T15:03:24Z",
  "total_alive": 5,
  "proxies": [
    {
      "ip": "213.163.196.45",
      "port": 80,
      "proxy": "213.163.196.45:80",
      "protocol": "http",
      "latency_sec": 0.551,
      "latency_ms": 551,
      "egress_ip": "213.163.196.45",
      "country": "Singapore",
      "country_code": "SG",
      "city": "Singapore",
      "isp": "UpCloud Ltd"
    }
  ]
}
```

### 2. `output/live_urls.txt`
Ready to feed into cURL, scraping bots, or browser profiles:
```text
http://213.163.196.45:80
http://163.181.207.227:9999
socks5://198.199.86.11:3128
```

### 3. `output/proxies.csv`
Tabular format compatible with Microsoft Excel, Google Sheets, or Pandas.

---

## 🤖 Free Automated Hosting with GitHub Actions

This repository includes [`.github/workflows/auto_harvest.yml`](.github/workflows/auto_harvest.yml). When you push this project to GitHub:
1. GitHub Actions will trigger automatically **every 6 hours** on Ubuntu runners.
2. It fetches, validates, and pushes the freshly verified `output/` files back to your repository.
3. You get a **100% free, perpetually updated proxy API/raw link** hosted directly on your GitHub repository!

---

## 🇮🇩 Panduan Singkat (Bahasa Indonesia)

Untuk pengguna di Indonesia:
- **Tujuan Tool:** Mengunduh 100.000+ proxy gratis dari 30+ sumber publik, mengetes kecepatan aslinya secara live, dan menyimpan proxy yang benar-benar aktif (bebas proxy mati).
- **Format:** Tersedia dalam teks biasa (`ip:port`), URL (`http://ip:port` / `socks5://...`), file JSON lengkap dengan data negara dan ISP, serta file CSV.
- **Dukungan 9Router & AI Scraper:** Bisa langsung memasukkan proxy aktif ke database 9Router via perintah:
  ```bash
  python main.py --sync-9router auto
  ```
- **Otomatisasi:** Bisa dibiarkan jalan di background tiap 20 menit dengan menambahkan `--loop 20`.

---

## ⚖️ Ethical Use & Disclaimer

This tool collects exclusively **public open-source proxy lists** that are already published publicly on the internet. It does not exploit, port scan, or hack any private systems. The authors are not responsible for any misuse. Users are responsible for adhering to applicable laws and website terms of service when routing traffic through public proxies.

---

## 📄 License

Released under the permissive **[MIT License](LICENSE)**. Feel free to use, modify, and distribute for personal and commercial projects!
