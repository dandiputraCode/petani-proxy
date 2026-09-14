<div align="center">

# 🌾 PetaniProxy v1.0
### *Local Rotating Proxy Gateway & Residential Hunter*
> Panen proxy publik dan residential gratis, ubah jadi satu gateway lokal `127.0.0.1:8888` yang otomatis muter tiap request. 🚜

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Maintainer](https://img.shields.io/badge/maintainer-itzluthfi-blueviolet.svg)](https://github.com/itzluthfi)
[![Protocols](https://img.shields.io/badge/protocols-HTTP%20%7C%20HTTPS%20%7C%20SOCKS4%20%7C%20SOCKS5-green.svg)](#-protokol--fitur-filter)
[![Rotating Gateway](https://img.shields.io/badge/gateway-127.0.0.1%3A8888-brightgreen.svg)](#2-jalankan-local-forward-gateway-port-8888)

<br>

```text
  ██████╗ ███████╗████████╗ █████╗ ███╗   ██╗██╗██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗
  ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗████╗  ██║██║██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
  ██████╔╝█████╗     ██║   ███████║██╔██╗ ██║██║██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ 
  ██╔═══╝ ██╔══╝     ██║   ██╔══██║██║╚██╗██║██║██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  
  ██║     ███████╗   ██║   ██║  ██║██║ ╚████║██║██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   
  ╚═╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
              🌾 PetaniProxy: Panen Proxy Cepat, Segar & Bersih 🚜
```

**PetaniProxy** itu tool buat lu yang capek nyari proxy gratisan tapi pas dipake malah mampus atau kena blok Cloudflare 403. Tool ini memanen ribuan proxy publik dari 30+ sumber global, nyaring yang beneran hidup dan anonim, terus nyediain satu pintu gerbang lokal di `http://127.0.0.1:8888`. Begitu lu tembak, IP bakal otomatis muter sendiri tiap request.

</div>

---

## Kenapa Bikin PetaniProxy?

Pernah ga lu lagi asyik scraping web atau jalanin bot akun, baru beberapa menit tau-tau kena **HTTP 403 Forbidden** atau **429 Too Many Requests**? Mau langganan proxy residential komersial harganya sering ga masuk akal buat project sampingan.

| Fitur | Proxy Gratisan Biasa | Proxy Berbayar ($$$) | 🌾 PetaniProxy v1.0 |
| :--- | :---: | :---: | :---: |
| **Biaya** | Gratis tapi 90% mati | Ratusan ribu s/d jutaan / bulan | **100% Gratis** |
| **Cara Pakai** | File text `ip:port` manual | Forward Gateway & REST API | **Tinggal colok ke `127.0.0.1:8888`** |
| **Tipe IP (Tembus Cloudflare)** | Datacenter Publik (gampang kena 403) | Residential Asli | **Residential Asli (Webshare Hunter)** |
| **Kredensial IP** | Rebutan banyak orang | Privat `user:pass` | **Privat `user:pass` per akun** |
| **Bypass Captcha** | Manual pusing sendiri | Kudu bayar saldo solver | **Audio Solver Bawaan (Gratis)** |
| **Rotasi IP** | Manual gonta-ganti di script | Otomatis | **Auto-rotate tiap request + retry 3x** |
| **Anonimitas** | Sering bocor IP asli | Tergantung paket | **Deteksi Elite L1 (Zero Leak)** |
| **Integrasi 9Router** | Harus bikin script sendiri | Tidak ada | **Auto-inject ke `data.sqlite`** |

---

## ⭐ [MVP] Fitur Utama: Webshare Residential Hunter

Kalau target scraping lu diproteksi Cloudflare Turnstile atau bot detector ketat, proxy publik biasa pasti langsung mental. Fitur ini dibuat buat dapetin **IP Residential (Perumahan)** dari Webshare secara otomatis:

- **100% Gratis (Audio Captcha Solver Bawaan)**: Menggunakan speech recognition (`SpeechRecognition` + `pydub`) buat mecahin captcha suara Google/hCaptcha secara otomatis. Lu ga perlu beli saldo API key solver pihak ketiga.
- **Bisa Pakai CapSolver (Opsional)**: Buat yang punya saldo di [CapSolver](https://www.capsolver.com), tinggal set environment variable `CAPSOLVER_API_KEY` buat mode headless yang lebih ngebut. Tapi default-nya tetap gratis tanpa biaya token.
- **Human-like Bezier Cursor**: Gerakan kursor pas daftar akun niru pergerakan tangan manusia biar lolos deteksi bot browser.
- **IP Residential Asli**: Dikenali sebagai ISP rumahan biasa, lebih tahan terhadap filter ketat di Grok AI, Twitter/X, Qoder, e-commerce, dsb.
- **Kredensial Privat**: Format yang didapat `http://user:pass@ip:port`, jadi bandwidth dan sesi ga bakal tabrakan sama user lain.
- **Auto-Sync ke 9Router**: Hasil panen langsung masuk ke database SQLite 9Router lokal (`data.sqlite`).

---

## Mode Penggunaan & Racikan Siap Pakai

### 1. Local Rotating Gateway (`127.0.0.1:8888`)
Lu ga perlu ngotak-ngatik ribuan baris IP di script lu. Cukup arahin script bot/scraper lu ke satu port:
- `[W]` ⭐ **Webshare Hunter (MVP)**: Panen 10-30 IP residential privat buat nembus proteksi tinggi.
- `[1]` **Racikan Ternak Akun**: Khusus bot AI (Grok, Qoder, dll). Filter ketat Elite L1, latency rendah, langsung sync ke 9Router.
- `[2]` **Racikan Scraper Barbar**: Pool 30+ IP aktif, rotasi ganti IP tiap request, cocok buat scraping e-commerce skala besar.
- `[3]` **Racikan Kencang Anti-Lag**: Filter ping terendah (<350ms) dari node SG, ID, dan US.
- `[4]` **Mode AFK 24 Jam**: Script jalan terus di background buat auto-refresh pool proxy tiap 15 menit.

### 2. Ekspor File Mentah
Kalau lu butuh file mentahan buat disuntik ke software lain (Proxifier, OpenBullet, script manual):
- `output/webshare_residential.txt` (Daftar IP Residential privat)
- `output/live_all.txt` & `output/live_urls.txt` (IP:Port & format URL Scheme)
- `output/live_elite.txt` (Khusus IP yang lolos uji penyamaran High Anonymity)
- `output/proxies.json` & `output/proxies.csv` (Lengkap dengan data negara, kota, ISP, dan latency)

### 3. Tes Penyamaran IP [T]
- `[T]` **Live Proof Masking**: Fitur di menu buat ngetes langsung apakah IP asli lu beneran ketutup atau masih bocor lewat port 8888.

---

## Cara Pasang (Instalasi)

```bash
# 1. Clone repositori ini
git clone https://github.com/itzluthfi/petani-proxy.git
cd petani-proxy

# 2. Pasang dependencies
pip install -r requirements.txt
```

> Buat pengguna Windows: Lu tinggal double-click file **`run.bat`**. Dia bakal otomatis ngecek Python, install paket yang belum ada, dan langsung ngebuka menu interaktif.

---

## Cara Penggunaan

### 1. Menu Interaktif
Tinggal jalanin tanpa argumen tambahan:
```bash
python main.py
```
Tinggal pilih opsi **`[W]`** buat panen Residential Proxy atau opsi racikan lainnya.

### 2. Jalankan Local Forward Gateway (Port 8888)
```bash
python main.py --serve 8888 --target 20
```
Tembak request scraper/bot lu ke gateway ini:
```bash
# Tes rotasi IP via terminal:
curl -x http://127.0.0.1:8888 https://api.ipify.org
```

### 3. Akses REST API Gateway
* `GET http://127.0.0.1:8888/api/random` — Ambil 1 proxy acak yang lagi hidup dan cepat.
* `GET http://127.0.0.1:8888/api/all` — Ambil seluruh daftar pool proxy aktif dalam format JSON.
* `GET http://127.0.0.1:8888/api/status` — Cek statistik pool, jumlah request sukses, dan persentase proxy aktif.

---

## Protokol & Fitur Filter Negara

PetaniProxy mendukung protokol **HTTP, HTTPS, SOCKS4, SOCKS5** dan dapat menyaring proxy dari **150+ negara di seluruh dunia** (menggunakan engine geolokasi ISO 3166-1 alpha-2 otomatis).

Tabel di bawah adalah contoh cheat sheet kode negara yang sering dipanen:

| Wilayah | Negara | Bendera | Kode ISO | Contoh Perintah CLI |
| :--- | :--- | :---: | :---: | :--- |
| **Asia Tenggara** | Indonesia | <img src="https://flagcdn.com/20x15/id.png" width="20" alt="ID"> | `ID` | `python main.py --country ID --target 10` |
| | Singapura | <img src="https://flagcdn.com/20x15/sg.png" width="20" alt="SG"> | `SG` | `python main.py --country SG --target 10` |
| | Malaysia | <img src="https://flagcdn.com/20x15/my.png" width="20" alt="MY"> | `MY` | `python main.py --country MY --target 10` |
| | Thailand | <img src="https://flagcdn.com/20x15/th.png" width="20" alt="TH"> | `TH` | `python main.py --country TH --target 10` |
| | Vietnam | <img src="https://flagcdn.com/20x15/vn.png" width="20" alt="VN"> | `VN` | `python main.py --country VN --target 10` |
| | Filipina | <img src="https://flagcdn.com/20x15/ph.png" width="20" alt="PH"> | `PH` | `python main.py --country PH --target 10` |
| **Asia Timur & Selatan** | Jepang | <img src="https://flagcdn.com/20x15/jp.png" width="20" alt="JP"> | `JP` | `python main.py --country JP --target 10` |
| | Korea Selatan | <img src="https://flagcdn.com/20x15/kr.png" width="20" alt="KR"> | `KR` | `python main.py --country KR --target 10` |
| | Hong Kong | <img src="https://flagcdn.com/20x15/hk.png" width="20" alt="HK"> | `HK` | `python main.py --country HK --target 10` |
| | India | <img src="https://flagcdn.com/20x15/in.png" width="20" alt="IN"> | `IN` | `python main.py --country IN --target 10` |
| **Amerika & Oceania** | Amerika Serikat | <img src="https://flagcdn.com/20x15/us.png" width="20" alt="US"> | `US` | `python main.py --country US --target 20` |
| | Kanada | <img src="https://flagcdn.com/20x15/ca.png" width="20" alt="CA"> | `CA` | `python main.py --country CA --target 10` |
| | Brasil | <img src="https://flagcdn.com/20x15/br.png" width="20" alt="BR"> | `BR` | `python main.py --country BR --target 10` |
| | Australia | <img src="https://flagcdn.com/20x15/au.png" width="20" alt="AU"> | `AU` | `python main.py --country AU --target 10` |
| **Eropa** | Jerman | <img src="https://flagcdn.com/20x15/de.png" width="20" alt="DE"> | `DE` | `python main.py --country DE --target 10` |
| | Inggris (UK) | <img src="https://flagcdn.com/20x15/gb.png" width="20" alt="GB"> | `GB` | `python main.py --country GB --target 10` |
| | Belanda | <img src="https://flagcdn.com/20x15/nl.png" width="20" alt="NL"> | `NL` | `python main.py --country NL --target 10` |
| | Prancis | <img src="https://flagcdn.com/20x15/fr.png" width="20" alt="FR"> | `FR` | `python main.py --country FR --target 10` |
| | Rusia | <img src="https://flagcdn.com/20x15/ru.png" width="20" alt="RU"> | `RU` | `python main.py --country RU --target 10` |

> 💡 **Mau negara lainnya?** Lu bisa pakai **kode ISO 2 huruf negara mana saja di dunia** (misal: Turki = `TR`, Italia = `IT`, Spanyol = `ES`, Taiwan = `TW`, dll). Sistem otomatis mendeteksi dan menyaring IP sesuai negara yang lu minta!

Bisa juga digabung dengan filter protokol:
```bash
# Contoh: Panen khusus SOCKS5 region Amerika Serikat (US)
python main.py --protocol socks5 --country US --target 10

# Contoh: Panen khusus HTTP region Singapura (SG)
python main.py --protocol http --country SG --target 15
```

---

## Traktir Kopi Sang Petani (Donasi / Support) ☕

Kalo PetaniProxy ngebantu lu ngurangin pengeluaran sewa proxy atau bikin project bot & scraping lu berjalan lancar, lu bisa support gw dengan traktir kopi lewat QRIS di bawah:

<div align="center">

<img src="assets/sticker.png" width="220" alt="DAHSYAT Meme">

<br>
<i>"Proxy lancar, kuota aman, hati tenang. DAHSYAT!"</i>
<br><br>

<img src="assets/qris.png" width="280" alt="QRIS Donasi PetaniProxy">

<br><br>
<b>Bisa scan via BCA, GoPay, OVO, DANA, ShopeePay, LinkAja, atau Mobile Banking apa aja.</b><br>
<sub>Atas Nama: <b>Luthfi Shidqi Habibulloh (Digital & Kreatif)</b> • NMID: <code>ID1026591157593</code></sub>

</div>

---

## Attribution & Credits (CC BY)

Proyek ini terinspirasi dari basis ide scraper milik:
* **[@hirotomasato](https://github.com/hirotomasato)** — Pengembang yang menginisiasi konsep dasar scraper awal.

### Bedanya PetaniProxy v1.0 dibanding repo upstream:
* **100% Gratis (Audio Captcha Solver)**: Di upstream biasanya butuh API key solver berbayar. Di PetaniProxy udah ada speech recognition bawaan yang mecahin captcha suara secara gratis tanpa perlu saldo.
* **Opsi CapSolver Tetap Disediakan**: Buat yang pengen proses headless lebih ngebut dan punya akun [CapSolver](https://www.capsolver.com), opsi `CAPSOLVER_API_KEY` tetap tersedia.
* **Integrasi 9Router Otomatis**: Hasil panen langsung di-inject ke database SQLite 9Router lokal (`data.sqlite`).
* **Local Rotating Gateway**: Nyediain forward proxy di `127.0.0.1:8888` lengkap dengan failover retry 3x.

---

## Author & Maintainer

* **itzluthfi**: [GitHub Profile](https://github.com/itzluthfi)
* Pull request, feedback, dan bintang (⭐ star) di repo ini sangat diapresiasi!

---

## Lisensi

Dilisensikan di bawah [MIT License](LICENSE).  
Copyright (c) 2026 itzluthfi. Atribusi ke kontributor upstream di bawah lisensi Creative Commons (CC BY).
