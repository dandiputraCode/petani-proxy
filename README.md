<div align="center">

# OmniProxy Harvester

**High-speed multi-protocol proxy scraper, validator, and GeoIP enricher.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Protocols](https://img.shields.io/badge/protocols-HTTP%20%7C%20HTTPS%20%7C%20SOCKS4%20%7C%20SOCKS5-green.svg)](#supported-protocols)
[![GitHub Actions](https://img.shields.io/badge/actions-automated%20harvest-brightgreen.svg)](.github/workflows/auto_harvest.yml)

OmniProxy Harvester concurrently extracts, deduplicates, and benchmarks public proxy lists from 30+ open-source upstream feeds. It tests real-world handshake latency against live endpoints, resolves country codes and ISP information, and outputs verified lists in TXT, JSON, and CSV.

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

## Features

- **Large-Scale Aggregation**: Harvests **115,000+ unique candidates** across 30+ feeds in under 3 seconds.
- **Multi-Protocol Support**: Handles **HTTP**, **HTTPS**, **SOCKS4**, and **SOCKS5**.
- **Real-Time Handshake Benchmarking**: Measures accurate round-trip latency (in milliseconds) against live endpoints (`https://api.ipify.org`).
- **GeoIP & ASN Resolution**: Resolves country code, country name, city, and ISP for alive proxies using batch requests.
- **Target-Driven Early Stop**: Halts validation as soon as your requested quota of live nodes is met.
- **Multi-Format Export**: Generates plain text lists, URL lists (`protocol://ip:port`), structured JSON, and CSV tables.
- **Automation Ready**: Pre-configured GitHub Actions workflow runs every 6 hours to maintain fresh proxy lists in your repository.
- **9Router Integration**: Direct database injection into 9Router SQLite proxy pools via `--sync-9router`.

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

OmniProxy Harvester detects and filters proxies across 150+ ISO country codes. You can target specific regions using the `--country` flag:

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

OmniProxy Harvester aggregates public open-source proxy lists. All endpoints are configured in [`config/sources.json`](config/sources.json):

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
git clone https://github.com/your-username/omni-proxy-harvester.git
cd omni-proxy-harvester
pip install -r requirements.txt
```

---

## Usage

### 1. Basic Harvest
Validate candidates across all protocols and find 15 live proxies:
```bash
python main.py
```

### 2. Protocol Filtering
Filter specifically for SOCKS5 or HTTP proxies:
```bash
python main.py --protocol socks5 --target 20 --timeout 2.5
python main.py --protocol http --target 25
```

### 3. Country Filtering
Target proxies within a designated country code:
```bash
python main.py --country US --target 10
python main.py --country SG --target 10
python main.py --country ID --target 5
```

### 4. Continuous Background Daemon
Run a scheduled sweep every 30 minutes:
```bash
python main.py --loop 30 --target 30
```

### 5. 9Router SQLite Sync
Sync live proxies directly into 9Router:
```bash
python main.py --sync-9router auto
```

---

## CLI Options Reference

```text
usage: main.py [-h] [--protocol {all,http,socks4,socks5}] [--max MAX]
               [--target TARGET] [--timeout TIMEOUT] [--workers WORKERS]
               [--country COUNTRY] [--loop LOOP] [--output OUTPUT]
               [--sync-9router SYNC_9ROUTER]

options:
  -h, --help            Show this help message and exit
  --protocol, -p        Target proxy protocol: all, http, socks4, socks5 (default: all)
  --max, -m             Maximum candidate proxies to test (default: 250)
  --target, -t          Target number of alive proxies to collect (default: 15)
  --timeout             Connection timeout in seconds (default: 3.0)
  --workers, -w         Concurrent testing workers (default: 50)
  --country, -c         Filter by ISO 2-letter country code (e.g. US, SG, ID, DE)
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
   https://raw.githubusercontent.com/<user>/<repo>/main/output/live_all.txt
   ```

---

## Disclaimer

This project collects and tests publicly accessible proxy lists for research, automation testing, and network diagnostic purposes. The maintainers do not operate or control these proxies and assume no liability for their use. Users are responsible for complying with local regulations and target website terms of service.

---

## License

Licensed under the [MIT License](LICENSE).
