<div align="center">

# 🌾 PetaniProxy v1.0
### *Pusat Amunisi Proxy Bersih, Segar & Berputar Otomatis (Local Rotating Gateway)*
> **"Kenapa mesti bayar sewa proxy residensial $500/bulan kalau bisa panen IP gratisan sambil ngopi santai?"** 🚜☕

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Maintainer](https://img.shields.io/badge/maintainer-itzluthfi-blueviolet.svg)](https://github.com/itzluthfi)
[![Protocols](https://img.shields.io/badge/protocols-HTTP%20%7C%20HTTPS%20%7C%20SOCKS4%20%7C%20SOCKS5-green.svg)](#-supported-protocols)
[![Rotating Gateway](https://img.shields.io/badge/gateway-127.0.0.1%3A8888-brightgreen.svg)](#-local-rotating-proxy-server--rest-api-gateway)
[![9Router Ready](https://img.shields.io/badge/sync-9Router%20%2F%20BansosRouter-orange.svg)](#-9router-sqlite-sync)

<br>

```text
  ██████╗ ███████╗████████╗ █████╗ ███╗   ██╗██╗██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
  ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗████╗  ██║██║██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
  ██████╔╝█████╗     ██║   ███████║██╔██╗ ██║██║██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
  ██╔═══╝ ██╔══╝     ██║   ██╔══██║██║╚██╗██║██║██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
  ██║     ███████╗   ██║   ██║  ██║██║ ╚████║██║██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
  ╚═╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
              🌾 PetaniProxy: Panen Proxy Cepat, Segar & Bergizi 🚜
```

**PetaniProxy** memanen, menyaring deduplikasi, dan memvalidasi ribuan proxy publik dari 30+ sumber upstream global dalam hitungan detik. Mengubah tumpukan IP mentah yang cepat mati menjadi satu pintu gerbang forward proxy lokal yang stabil di `http://127.0.0.1:8888` layaknya layanan proxy komersial mahal.

</div>

---

## 🥊 Mengapa Harus PetaniProxy? (Realita Lapangan)

Pernah ga sih lu lagi asyik scraping data atau botting akun, baru jalan 3 menit tau-tau kena **HTTP 403 Forbidden** atau **429 Too Many Requests** dari Cloudflare? Nah, tabel ini alasan kenapa PetaniProxy diciptakan:

| Fitur / Kemampuan | Proxy Gratisan Biasa 💩 | Layanan Komersial ($500/bln) 💸 | 🌾 **PetaniProxy v1.0** 👑 |
| :--- | :---: | :---: | :---: |
| **Biaya Bulanan** | Gratis (tapi bikin emosi) | Rp 1,5 Juta – 7 Juta/bulan | **100% GRATIS & Bebas Batas** |
| **Bentuk Akses** | File teks `ip:port` mentah | Forward Gateway & REST API | **Local Rotating Gateway (`127.0.0.1:8888`)** |
| **Tipe IP (Bypass Cloudflare)** | ❌ Datacenter Publik (Sering 403) | ✅ Residential ($$$ Mahal) | ✅ **IP Residential Asli (Webshare Hunter)** |
| **Kredensial IP** | ❌ Rebutan sejuta umat (Cepat mati) | ✅ Privat `user:pass` | ✅ **Privat `user:pass` per Akun (Stabil)** |
| **Auto-Solve Captcha** | ❌ Buntu, suruh pecahin sendiri | ❌ Bayar saldo token solver | ✅ **Built-in AI Audio Solver (100% Gratis)** |
| **Rotasi IP Otomatis** | ❌ Manual gonta-ganti IP di kodingan | ✅ Otomatis | ✅ **Auto-Rotate Setiap Request + Failover 3x** |
| **Uji Anonimitas (Zero Leak)**| ❌ Jarang ada, IP asli bocor | ✅ Ada | ✅ **Built-in Elite L1 Detection** |
| **Live Proof Masking [T]** | ❌ Ga ada pembuktian | ❌ Ga ada | ✅ **1-Click Test Perbandingan IP Asli** |
| **Integrasi AI Router** | ❌ Kudu ngoding script sendiri | ❌ Ga kepikiran | ✅ **Auto-Inject langsung ke 9Router DB** |

---

## ⭐ [MVP] Fitur Bintang: Webshare Residential Hunter 🏢
> *"Solusi mujarab buat yang tensinya langsung naik tiap liat Cloudflare Turnstile muter-muter tanpa henti."*

Kebanyakan proxy scraper gratisan cuma ngambil IP datacenter publik yang udah masuk daftar hitam Cloudflare. **Webshare Hunter** hadir sebagai senjata pamungkas untuk memanen **IP Perumahan Asli (Genuine Residential Proxies)** secara full-otomatis:

### 🎯 Kenapa Ini Jadi Senjata MVP?
* 🧠 **100% GRATIS Tanpa Keluar Duit Token**: Dilengkapi **AI Audio Captcha Solver** (`SpeechRecognition` + `pydub`). Dia bakal dengerin suara captcha Google/hCaptcha dan ngetik jawabannya otomatis tanpa lu perlu beli saldo solver!
* 🎛️ **Bisa Pakai CapSolver (Opsional)**: Buat lu yang sultan dan punya saldo [CapSolver](https://www.capsolver.com), lu bisa pasang `CAPSOLVER_API_KEY` buat solving headless super ngebut. Tapi ingat, **default-nya tetap 100% GRATIS**!
* 🖱️ **Gerakan Kursor Kurva Bezier Manusia**: Bot meniru ayunan tangan manusia saat mengklik form pendaftaran, bikin sistem anti-bot terkecoh mengira lu manusia beneran.
* 🏠 **IP Rumah Asli (Bukan Datacenter)**: Dikenali sebagai ISP rumahan biasa, sehingga **kebal filter ketat** di Grok AI, Twitter/X, Qoder, Shopee, Tokopedia, dan berbagai provider AI lainnya.
* 🔑 **Kredensial Privat**: Lengkap dengan format `http://user:pass@ip:port`, anti-rebutan bandwidth sama orang lain.
* 🔄 **Auto-Suntik ke 9Router**: Sekali panen kelar, proxy langsung nongol di database 9Router lokal (`data.sqlite`).

---

## 🎯 3 Pilar Arsitektur & Racikan Spesial

### [Pilar 1] 🚀 Instant Rotating Gateway (`127.0.0.1:8888`)
Lu ga perlu pusing masukin ribuan IP ke kodingan lu. Cukup arahkan scraper atau bot lu ke **`http://127.0.0.1:8888`**, dan PetaniProxy yang bakal giliran muter IP hidup secara cerdas:
* `[W]` ⭐ **Webshare Hunter (MVP)**: Panen 10-30 IP perumahan asli ber-kredensial privat tembus proteksi tinggi.
* `[1]` 🐔 **Racikan Ternak Akun**: Khusus peternak bot AI (Grok, Qoder, dll). Filter ketat Elite L1, latency kencang (<2.5s), auto-sync ke 9Router.
* `[2]` 🕷️ **Racikan Scraper Barbar**: Amunisi pool 30+ IP aktif, rotasi ganti IP tiap request, anti-block e-commerce.
* `[3]` ⚡ **Racikan Ngacir Anti-Lag**: Filter ping terendah (<350ms) dari node SG, ID, dan US buat bypass internet positif.
* `[4]` 🚜 **Mode Petani AFK 24 Jam**: Tinggal tidur atau ngopi, biarkan komputer lu auto-pilot panen & refresh pool tiap 15 menit.

### [Pilar 2] 📥 Bungkus File Mentah
Buat yang butuh file mentahan buat disuntikkan ke software bot lain:
* `output/webshare_residential.txt` (Daftar IP Residential privat)
* `output/live_all.txt` & `output/live_urls.txt` (IP:Port & format URL Scheme)
* `output/live_elite.txt` (Khusus IP yang lolos uji penyamaran High Anonymity)
* `output/proxies.json` & `output/proxies.csv` (Lengkap dengan data negara, kota, ISP & latency)

### [Pilar 3] 🛠️ Bengkel Oprek & Tes Kesaktian [T]
* `[T]` **Uji Kesaktian Topeng (Live Proof)**: Buktiin langsung apakah IP asli lu beneran ketutup rapat lewat Gateway 8888.
* `[M]` **Oprek Suka-Suka**: Bebas pilih protokol (SOCKS5/HTTP), sortir negara tertentu (ID, US, SG), atau tembak URL target khusus.

---

## ⚡ Cara Pasang (Instalasi Cepat)

```bash
# 1. Clone repositori ini
git clone https://github.com/itzluthfi/petani-proxy.git
cd petani-proxy

# 2. Pasang dependencies
pip install -r requirements.txt
```

> 💡 **Buat Pengguna Windows Awam:** Cukup klik ganda file **`run.bat`**! Dia bakal otomatis mendeteksi Python, memasang paket yang kurang, dan membuka menu interaktif.

---

## 🚀 Cara Penggunaan

### 1. Menu Interaktif (Paling Santai & Praktis)
Tinggal jalankan tanpa argumen:
```bash
python main.py
```
Pilih opsi **`[W]`** buat panen Residential Proxy atau **`[1]`** buat forward gateway.

### 2. Jalankan Local Forward Gateway (Port 8888)
```bash
python main.py --serve 8888 --target 20
```
Tembak request bot/scraper lu ke port ini:
```bash
# Tes rotasi IP via terminal:
curl -x http://127.0.0.1:8888 https://api.ipify.org
```

### 3. Akses REST API Bawaan
* `GET http://127.0.0.1:8888/api/random` — Ambil 1 proxy acak yang lagi hidup dan kencang.
* `GET http://127.0.0.1:8888/api/all` — Ambil seluruh daftar pool proxy aktif dalam JSON.
* `GET http://127.0.0.1:8888/api/status` — Cek statistik pool, jumlah request sukses, dan persentase proxy aktif.

### 4. Filter Negara & Protokol Tertentu
```bash
# Panen khusus SOCKS5 region Amerika Serikat (US):
python main.py --protocol socks5 --country US --target 10

# Panen khusus HTTP region Indonesia (ID):
python main.py --protocol http --country ID --target 5
```

---

## 🌐 Supported Protocols & Feeds

* **Protokol:** HTTP, HTTPS, SOCKS4, SOCKS5.
* **Jangkauan Negara:** Mendukung 150+ ISO Country Codes (`ID`, `SG`, `US`, `DE`, `JP`, `KR`, dll).
* **Upstream Feeds:** Terintegrasi dengan 30+ feed global terpercaya (ProxyScrape, TheSpeedX, monosans, hookzof, roosterkid, dll).

---

## ☕ Traktir Kopi Buat Sang Petani (Donasi / Support)

> *"Coding butuh kopi, server butuh amunisi, dan petani butuh apresiasi. Hehe."* 💸

Kalau **PetaniProxy** ngebantu lu nembus Cloudflare, ngirit ratusan dollar biaya langganan proxy komersial, atau bikin proyek scraping & bot lu makin lancar jaya, boleh banget disisihkan recehnya buat traktir segelas kopi hitam atau beli amunisi riset:

<div align="center">

<br>

<img src="assets/qris.png" width="280" alt="QRIS Donasi PetaniProxy" onerror="this.src='https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=https%3A%2F%2Fgithub.com%2Fitzluthfi%2Fpetani-proxy';">

<br>
<b>Scan QRIS via BCA, GoPay, OVO, DANA, ShopeePay, LinkAja, atau Mobile Banking apa aja!</b>

<br>
<sub><i>(Punya file QRIS sendiri? Cukup letakkan gambar QRIS Anda di <code>assets/qris.png</code>, otomatis tampil di sini!)</i></sub>

</div>

---

## 🙏 Acknowledgements & Attribution (CC BY)

Proyek ini terinspirasi dan dikembangkan dengan memanfaatkan basis fondasi karya hebat dari:
* **[@hirotomasato](https://github.com/hirotomasato)** — Kontributor & developer yang menginisiasi konsep dasar scraper awal.

### 💡 Apa Bedanya PetaniProxy v1.0 dengan Upstream?
* **100% GRATIS Tanpa Biaya Token Captcha**: Upstream umumnya membutuhkan saldo API solver pihak ketiga. PetaniProxy menyertakan **Built-in AI Speech Recognition Audio Solver** yang 100% gratis tanpa bayar sepeser pun.
* **Dukungan CapSolver Opsional**: Bagi pengguna pro yang ingin kecepatan headless ekstra, opsi [CapSolver](https://www.capsolver.com) tetap disediakan (`CAPSOLVER_API_KEY`). Tapi default bawaannya tetap gratis tanpa biaya token.
* **Integrasi AI Router Langsung**: Otomatis menyuntikkan proxy hasil panen ke database SQLite 9Router (`data.sqlite`).
* **Local Rotating Gateway**: Menjalankan forward proxy lokal di `127.0.0.1:8888` lengkap dengan failover retry 3x.

---

## 👨‍🌾 Author & Maintainer

* **itzluthfi**: [GitHub Profile](https://github.com/itzluthfi)
* Pull requests, saran racikan baru, dan bintang (⭐ star) di repo ini sangat diapresiasi!

---

## 📜 Disclaimer & License

Proyek ini dibuat untuk tujuan riset, pengujian otomatisasi, dan diagnostik jaringan. Pengguna bertanggung jawab penuh atas kepatuhan terhadap hukum setempat dan ketentuan layanan situs target.

Dilisensikan di bawah [MIT License](LICENSE).  
Copyright (c) 2026 itzluthfi. Atribusi ke kontributor upstream di bawah lisensi Creative Commons (CC BY).
