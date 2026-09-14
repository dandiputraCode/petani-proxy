<div align="center">

# 🌾 PetaniProxy v1.0

**Pusat Amunisi Proxy Bersih, Segar & Berputar Otomatis (Local Rotating Gateway).**  
*High-Speed Multi-Protocol Scraper, Validator, Self-Healing Pool & REST API.*

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Maintainer](https://img.shields.io/badge/maintainer-itzluthfi-blueviolet.svg)](https://github.com/itzluthfi)
[![Protocols](https://img.shields.io/badge/protocols-HTTP%20%7C%20HTTPS%20%7C%20SOCKS4%20%7C%20SOCKS5-green.svg)](#supported-protocols)
[![Rotating Gateway](https://img.shields.io/badge/gateway-127.0.0.1%3A8888-brightgreen.svg)](#local-rotating-proxy-server--rest-api-gateway)
[![BansosRouter Ready](https://img.shields.io/badge/sync-BansosRouter%20%2F%209Router-orange.svg)](#bansosrouter--9router-integration)

**PetaniProxy** secara otomatis memanen, menyaring deduplikasi, dan memvalidasi ribuan proxy publik dari 30+ sumber upstream global dalam hitungan detik. Mengubah ribuan IP mentah yang cepat mati menjadi satu pintu gerbang forward proxy lokal yang stabil di `http://127.0.0.1:8888` layaknya layanan proxy komersial ratusan dollar.

Created and maintained with ❤️ by [@itzluthfi](https://github.com/itzluthfi).

</div>

---

```
  ██████╗ ███████╗████████╗ █████╗ ███╗   ██╗██╗██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
  ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗████╗  ██║██║██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
  ██████╔╝█████╗     ██║   ███████║██╔██╗ ██║██║██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
  ██╔═══╝ ██╔══╝     ██║   ██╔══██║██║╚██╗██║██║██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
  ██║     ███████╗   ██║   ██║  ██║██║ ╚████║██║██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
  ╚═╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
```

---

## 🥊 Mengapa PetaniProxy? (Comparison Matrix)

| Fitur / Kemampuan | Proxy Gratisan Biasa | Layanan Komersial ($500/bln) | **🌾 PetaniProxy v1.0** |
| :--- | :---: | :---: | :---: |
| **Biaya** | Gratis (manual & ribet) | Rp 1,5 Juta – 7 Juta/bulan | **100% Gratis & Bebas Batas** |
| **Bentuk Akses** | File teks `ip:port` mentah | Forward Gateway & REST API | **Local Rotating Gateway (Port 8888)** |
| **Rotasi IP Otomatis** | ❌ Manual ganti IP | ✅ Otomatis | ✅ **Auto-Rotate Setiap Request** |
| **Uji Anonimitas (Zero Leak)**| ❌ Jarang ada | ✅ Ada | ✅ **Built-in Elite L1 Detection** |
| **Live Proof Masking [T]** | ❌ Tidak ada | ❌ Tidak ada | ✅ **1-Click Test Perbandingan IP Asli** |
| **Integrasi AI Router** | ❌ Bikin script sendiri | ❌ Tidak ada | ✅ **Auto-Inject BansosRouter & 9Router** |

---

## ⭐ [MVP] Fitur Bintang: Webshare Residential Hunter 🏢
> **Bosan dengan proxy publik gratisan yang cepat mati dan sering diblokir Cloudflare?**  
> **Webshare Hunter** adalah senjata pamungkas PetaniProxy untuk memanen **IP Perumahan Asli (Genuine Residential Proxies)** secara 100% otomatis dan gratis!

### 🎯 Mengapa Ini Menjadi Fitur MVP (Unggulan Utama)?
* 🧠 **100% GRATIS dengan AI Audio Captcha Solver**: Menggunakan voice recognition bawaan (`SpeechRecognition` + `pydub`) untuk memecahkan audio challenge reCAPTCHA secara lokal **tanpa bayar API captcha sepeser pun**.
* 🎛️ **Fleksibel (Dukungan CapSolver Berbayar)**: Bagi Anda yang punya saldo [CapSolver](https://www.capsolver.com) dan ingin solving lebih cepat secara headless, cukup set environment variable `CAPSOLVER_API_KEY`. PetaniProxy otomatis mendeteksinya, namun **DEFAULT-nya tetap 100% GRATIS**.
* 🖱️ **Human Mouse Movement (Kurva Bezier)**: Mengemulasikan gerakan mouse melengkung alami manusia saat pengisian form agar lolos sensor bot.
* 🏠 **IP Residential Rumah (Bukan Datacenter)**: Dikenali sebagai ISP rumahan biasa, sehingga **lolos proteksi ketat** di Grok AI, Twitter/X, Qoder, Shopee, Tokopedia, dan Cloudflare Protected Sites.
* 🔑 **Kredensial Privat**: Lengkap dengan `username:password` pribadi per IP, aman dan stabil tanpa rebutan bandwidth dengan orang lain.
* 🔄 **Auto-Sync 9Router / BansosRouter**: Hasil panen otomatis disuntikkan ke database SQLite 9Router lokal (`data.sqlite`) tanpa perlu input manual.

---

## 🎯 3 Pilar Arsitektur & Racikan Spesial

### [Pilar 1] 🚀 Instant Rotating Gateway (`127.0.0.1:8888`)
* `[W]` ⭐ **Webshare Residential Hunter (MVP)**: Panen otomatis 10-30 IP perumahan (Residential IP) gratis dengan AI Audio Captcha Solver untuk menembus Cloudflare Turnstile & registrasi high-security.
* `[1]` 🐔 **Racikan Ternak Akun**: Khusus bot registrasi AI (Grok, Qoder, Sosmed). Filter ketat Elite L1, latency rendah (<2.5s), dan otomatis menyuntikkan IP ke database 9Router.
* `[2]` 🕷️ **Racikan Scraper Brutal**: Pool 30+ IP aktif, rotasi IP tiap request, cocok untuk scraping marketplace & anti-block.
* `[3]` ⚡ **Racikan Turbo Surfing**: Filter khusus node SG/ID/US dengan ping terendah (<350ms) untuk bypass blokir & streaming.
* `[4]` 🚜 **Mode Petani 24 Jam**: Berjalan di latar belakang, otomatis memanen dan menyegarkan pool setiap 15 menit.

### [Pilar 2] 📥 Ekspor File Mentah
Ekspor instan ke berbagai format untuk software pihak ketiga:
* `output/live_all.txt` (IP:Port)
* `output/live_urls.txt` (URL Scheme)
* `output/live_elite.txt` (Hanya High Anonymity)
* `output/proxies.json` & `output/proxies.csv`

### [Pilar 3] 🛠️ Bengkel Oprek Manual & Uji Tembus [T]
* `[T]` **Live Identity Test**: Pembuktian langsung apakah IP asli tertutup sempurna lewat Gateway 8888.
* `[M]` **Bengkel Oprek**: Bebas memilih protokol SOCKS5/HTTP, menyaring negara tertentu (ISO ID, US, SG, dll), atau menembak URL target tertentu.

---

## Features

- **Large-Scale Aggregation**: Harvests **115,000+ unique candidates** across 30+ feeds in under 3 seconds.
- **Multi-Protocol Support**: Handles **HTTP**, **HTTPS**, **SOCKS4**, and **SOCKS5**.
- **Local Rotating Gateway**: Runs a local HTTP/HTTPS forward proxy on `127.0.0.1:8888` that automatically load-balances and rotates requests across live proxies.
- **Built-in REST API**: Instant endpoints (`/api/random`, `/api/all`, `/api/status`) for programmatic integration with bots and scrapers.
- **Anonymity Level Detection**: Classifies proxies into **Elite (High Anonymous)**, **Anonymous**, and **Transparent** by detecting header leaks.
- **Target-Specific Validation**: Tests proxies directly against custom endpoints (e.g. `--target-url https://google.com` or e-commerce sites).
- **Real-Time Handshake Benchmarking**: Measures round-trip latency in milliseconds against live endpoints.
- **GeoIP & ASN Resolution**: Resolves country code, country name, city, and ISP for alive proxies.
- **BansosRouter & 9Router Auto-Discovery**: Smart auto-detection for local SQLite proxy pools (`--sync-9router auto`).

---

## Real-World Use Cases

Why do developers, AI builders, and data teams rely on PetaniProxy?

1. **Large-Scale Web Scraping & Crawling**: Prevent `HTTP 429 Too Many Requests` and IP-bans on e-commerce, news, and directories by distributing traffic across rotating live nodes.
2. **AI & LLM API Load Balancing**: Route outbound AI requests across multiple upstream nodes to bypass per-IP rate limits on LLM reverse-proxies (e.g. Grok, Claude, Gemini, ChatGPT via 9Router).
3. **Multi-Account Automation & Botting**: Prevent account registration throttling and checkpoint bans by assigning isolated clean IPs to headless browser instances (Puppeteer, Playwright, Selenium).
4. **Geo-Targeted SEO & SERP Auditing**: Inspect localized Google search rankings and regional content as viewed from 150+ countries (`--country US`, `--country SG`, `--country ID`).
5. **Bypass Regional Throttling & Censorship**: Route browser traffic through clean regional nodes without needing heavy, expensive VPN subscriptions.
6. **Security Research & Pentesting**: Distribute directory fuzzing and API endpoint benchmarking across multiple egress nodes.

---

## Supported Protocols

| Protocol | Prefix | Best For | Status |
| :--- | :--- | :--- | :--- |
| **HTTP** | `http://` | Web scraping, standard REST APIs | Supported |
| **HTTPS** | `https://` | Secure web browsing, SSL tunneling | Supported |
| **SOCKS4** | `socks4://` | General TCP connections | Supported |
| **SOCKS5** | `socks5://` | High-speed TCP/UDP traffic, authentication, AI bots | Supported |

---

## Supported Countries

PetaniProxy detects and filters proxies across 150+ ISO country codes. You can target specific regions using the `--country` flag:

| Region | ISO Code | Country |
| :--- | :--- | :--- |
| 🇺🇸 North America | `US` | United States |
| 🇨🇦 North America | `CA` | Canada |
| 🇸🇬 Southeast Asia | `SG` | Singapore |
| 🇮🇩 Southeast Asia | `ID` | Indonesia |
| 🇻🇳 Southeast Asia | `VN` | Vietnam |
| 🇹🇭 Southeast Asia | `TH` | Thailand |
| 🇩🇪 Europe | `DE` | Germany |
| 🇳🇱 Europe | `NL` | Netherlands |
| 🇬🇧 Europe | `GB` | United Kingdom |
| 🇫🇷 Europe | `FR` | France |
| 🇷🇺 Europe / Asia | `RU` | Russia |
| 🇯🇵 East Asia | `JP` | Japan |
| 🇰🇷 East Asia | `KR` | South Korea |
| 🇮🇳 South Asia | `IN` | India |
| 🇧🇷 South America | `BR` | Brazil |
| 🇦🇺 Oceania | `AU` | Australia |

*And any valid 2-letter ISO 3166-1 alpha-2 country code.*

---

## Upstream Feed Sources

PetaniProxy aggregates public open-source proxy lists. All endpoints are configured in [`config/sources.json`](config/sources.json):

| Feed Provider | Upstream Source / Repo | Protocols | Type |
| :--- | :--- | :--- | :--- |
| **ProxyScrape** | [proxyscrape.com](https://proxyscrape.com) | HTTP, SOCKS4, SOCKS5 | REST API |
| **TheSpeedX** | [TheSpeedX/PROXY-List](https://github.com/TheSpeedX/PROXY-List) | HTTP, SOCKS4, SOCKS5 | Raw List |
| **monosans** | [monosans/proxy-list](https://github.com/monosans/proxy-list) | HTTP, SOCKS4, SOCKS5 | Raw List |
| **hookzof** | [hookzof/socks5_list](https://github.com/hookzof/socks5_list) | SOCKS5 | Raw List |
| **clarketm** | [clarketm/proxy-list](https://github.com/clarketm/proxy-list) | HTTP, HTTPS | Raw List |
| **roosterkid** | [roosterkid/openproxylist](https://github.com/roosterkid/openproxylist) | HTTPS, SOCKS4, SOCKS5 | Raw List |
| **sunny9577** | [sunny9577/proxy-scraper](https://github.com/sunny9577/proxy-scraper) | HTTP, HTTPS | Raw List |
| **ShiftyTR** | [ShiftyTR/Proxy-List](https://github.com/ShiftyTR/Proxy-List) | HTTP, HTTPS, SOCKS4, SOCKS5 | Raw List |
| **B4RC0DE-TM** | [B4RC0DE-TM/proxy-list](https://github.com/B4RC0DE-TM/proxy-list) | HTTP, SOCKS4, SOCKS5 | Raw List |
| **zevtyardt** | [zevtyardt/proxy-list](https://github.com/zevtyardt/proxy-list) | HTTP, SOCKS4, SOCKS5 | Raw List |
| **mertguvencli** | [mertguvencli/http-proxy-list](https://github.com/mertguvencli/http-proxy-list) | HTTP | Raw List |
| **hendrikbgr** | [hendrikbgr/Free-Proxy-Repo](https://github.com/hendrikbgr/Free-Proxy-Repo) | HTTP | Raw List |
| **RX007** | [RX007/Proxy-List](https://github.com/RX007/Proxy-List) | HTTP | Raw List |
| **almroot** | [almroot/proxylist](https://github.com/almroot/proxylist) | HTTP | Raw List |
| **manuGMG** | [manuGMG/proxy-365](https://github.com/manuGMG/proxy-365) | SOCKS5 | Raw List |

---

## Installation

```bash
git clone https://github.com/itzluthfi/petani-proxy.git
cd petani-proxy
pip install -r requirements.txt
```

---

## Usage

### 1. Interactive Terminal UI Mode
Simply launch without arguments for the styled interactive menu:
```bash
python main.py
```

### 2. Local Rotating Proxy Server & REST API Gateway
Start a local proxy gateway and REST API on port `8888`:
```bash
python main.py --serve 8888 --target 20
```
- **Forward Traffic**: Send your scraper or browser traffic to `http://127.0.0.1:8888`. PetaniProxy automatically rotates requests across verified live proxies.
  ```bash
  curl -x http://127.0.0.1:8888 https://api.ipify.org
  ```
- **REST API Endpoints**:
  - `GET http://127.0.0.1:8888/api/random` — Get a single fast live proxy.
  - `GET http://127.0.0.1:8888/api/all` — Get all alive proxies in JSON.
  - `GET http://127.0.0.1:8888/api/status` — Get pool health, request count, and uptime stats.

### 3. Filter by Anonymity Level
Filter strictly for High Anonymous (**Elite**) proxies with zero IP or header leaks:
```bash
python main.py --anonymity elite --target 15
```

### 4. Target-Specific Website Validation
Verify proxies directly against a custom website to ensure they are not blocked:
```bash
python main.py --target-url https://google.com --target 10
python main.py --target-url https://shopee.co.id --target 10
```

### 5. Protocol & Country Filtering
```bash
python main.py --protocol socks5 --country US --target 10
python main.py --protocol http --country ID --target 5
```

### 6. Continuous Background Daemon
Run a scheduled sweep every 30 minutes:
```bash
python main.py --loop 30 --target 30
```

### 7. 9Router SQLite Sync
Sync live proxies directly into 9Router:
```bash
python main.py --sync-9router auto
```

---

## CLI Options Reference

```text
usage: main.py [-h] [--protocol {all,http,socks4,socks5}] [--max MAX]
               [--target TARGET] [--timeout TIMEOUT] [--workers WORKERS]
               [--country COUNTRY]
               [--anonymity {all,elite,anonymous,transparent}]
               [--target-url TARGET_URL] [--serve [SERVE]] [--loop LOOP]
               [--output OUTPUT] [--sync-9router SYNC_9ROUTER]

options:
  -h, --help            Show this help message and exit
  --protocol, -p        Target proxy protocol: all, http, socks4, socks5 (default: all)
  --max, -m             Maximum candidate proxies to test (default: 250)
  --target, -t          Target number of alive proxies to collect (default: 15)
  --timeout             Connection timeout in seconds (default: 3.0)
  --workers, -w         Concurrent testing workers (default: 50)
  --country, -c         Filter by ISO 2-letter country code (e.g. US, SG, ID, DE)
  --anonymity           Filter by anonymity level: all, elite, anonymous, transparent
  --target-url          Validate proxies against specific website (default: api.ipify.org)
  --serve [PORT]        Start local rotating forward proxy & REST API (default port: 8888)
  --loop, -l            Auto-refresh loop interval in minutes (0 = single run)
  --output, -o          Custom output directory (default: output/)
  --sync-9router        Path to 9Router SQLite data.sqlite or 'auto'
```

---

## Output Structure

Verified nodes are stored under `output/`:

- **`output/live_all.txt`**: Plain text `ip:port` format.
- **`output/live_urls.txt`**: Protocol prefixed format (`http://...`, `socks5://...`).
- **`output/live_http.txt`**, **`output/live_socks4.txt`**, **`output/live_socks5.txt`**: Protocol-segmented lists.
- **`output/proxies.json`**: Full metadata including latency, country, and ISP.
- **`output/proxies.csv`**: Tabular CSV export.

### JSON Output Example
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

---

## Automated GitHub Actions Setup

This repository contains [`.github/workflows/auto_harvest.yml`](.github/workflows/auto_harvest.yml). Once pushed to GitHub:

1. The workflow runs on an Ubuntu runner every 6 hours.
2. It executes `main.py`, validates live nodes, and commits updated files in `output/`.
3. Your repository acts as a live, self-updating raw proxy endpoint:
   ```text
   https://raw.githubusercontent.com/itzluthfi/petani-proxy/main/output/live_all.txt
   ```

---

## 🙏 Acknowledgements & Attribution (CC BY)

Proyek ini terinspirasi dan dikembangkan dengan memanfaatkan basis fondasi karya hebat dari:
* **[@hirotomasato](https://github.com/hirotomasato)** — Kontributor & developer yang menginisiasi konsep dasar scraper awal.

### 💡 Keunggulan PetaniProxy v1.0 dibanding Upstream:
* **100% GRATIS Tanpa Biaya Token Captcha**: Upstream umumnya membutuhkan solver berbayar / ribet. PetaniProxy menyertakan **Built-in AI Speech Recognition Audio Solver** yang 100% gratis tanpa perlu berlangganan solver apapun!
* **Dukungan CapSolver Opsional**: Bagi pengguna pro yang ingin memakai API key [CapSolver](https://www.capsolver.com), opsi ini tetap disediakan (tinggal pasang `CAPSOLVER_API_KEY`). Namun, default bawaannya tetap 100% gratis tanpa setup tambahan.
* **Integrasi AI Router Langsung**: Otomatis menyuntikkan proxy hasil panen ke database SQLite 9Router (`data.sqlite`).
* **Local Rotating Gateway**: Menjalankan forward proxy lokal di `127.0.0.1:8888` dengan auto-failover retry 3x.

---

## Author & Maintainer

- **itzluthfi**: [GitHub Profile](https://github.com/itzluthfi)
- Pull requests, issues, and star contributions are welcome!

---

## Disclaimer

This project collects and tests publicly accessible proxy lists for research, automation testing, and network diagnostic purposes. The maintainers do not operate or control these proxies and assume no liability for their use. Users are responsible for complying with local regulations and target website terms of service.

---

## License

Licensed under the [MIT License](LICENSE).
Copyright (c) 2026 itzluthfi. Attributions to upstream contributors under Creative Commons (CC BY).
