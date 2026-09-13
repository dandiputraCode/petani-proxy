# OmniProxy Harvester — Panduan Lengkap Penggunaan (Usage Guide)

Panduan praktis cara menggunakan **OmniProxy Harvester**, cara kustomisasi jumlah panen (> 15, misal 50 atau 100 proxy), filter negara, penggunaan Local Rotating Gateway, dan integrasi ke bot/scraper.

---

## Daftar Isi
1. [Cara Menjalankan Menu Interaktif](#1-cara-menjalankan-menu-interaktif)
2. [Cara Panen Lebih dari 15 Proxy (Kustom Jumlah)](#2-cara-panen-lebih-dari-15-proxy-kustom-jumlah)
3. [Cara Menjalankan Local Rotating Proxy & REST API (Port 8888)](#3-cara-menjalankan-local-rotating-proxy--rest-api-port-8888)
4. [Cara Panen Khusus Proxy Tertentu](#4-cara-panen-khusus-proxy-tertentu)
   - [Khusus Proxy Elite (High Anonymous)](#a-khusus-proxy-elite-high-anonymous)
   - [Khusus Negara Tertentu (ID, SG, US, dll)](#b-khusus-negara-tertentu-id-sg-us-dll)
   - [Khusus Tembus Website Tertentu (Google, Shopee, dll)](#c-khusus-tembus-website-tertentu-google-shopee-dll)
5. [Cara Integrasi ke Script Python / Scraper / Bot](#5-cara-integrasi-ke-script-python--scraper--bot)
6. [Tabel Semua Perintah CLI Lengkap](#6-tabel-semua-perintah-cli-lengkap)

---

## 1. Cara Menjalankan Menu Interaktif

Buka terminal di folder proyek:
```powershell
cd D:\FREELANCE\omni-proxy-harvester
python main.py
```
Akan muncul menu bergaya kotak dengan watermark **`@itzluthfi`**. Anda cukup mengetik angka opsi yang diinginkan:
- `[1]` : Panen Cepat (Bebas input jumlah target, default: 15)
- `[2]` : Panen khusus SOCKS5
- `[3]` : Panen khusus HTTP / HTTPS
- `[4]` : Filter berdasarkan Kode Negara (ID, SG, US, JP, dll)
- `[5]` : Panen khusus Proxy Elite (100% tanpa bocor IP)
- `[6]` : Uji tembus ke target website tertentu
- `[7]` : Jalankan Local Rotating Proxy Server & REST API
- `[8]` : Auto-Refresh Daemon (Jalan otomatis tiap N menit)
- `[9]` : Sinkronisasi otomatis ke Database 9Router
- `[S]` : Lihat hasil panen terakhir
- `[0]` : Keluar

---

## 2. Cara Panen Lebih dari 15 Proxy (Kustom Jumlah)

### Opsi A: Lewat Menu Interaktif
1. Jalankan `python main.py`.
2. Pilih opsi `[1]` (atau `[2]`, `[3]`, `[5]`).
3. Saat terminal bertanya:
   ```text
   Target alive proxies count [default: 15]:
   ```
   Ketik jumlah yang Anda mau, misalnya **`50`** atau **`100`**, lalu tekan Enter.
   *Sistem akan otomatis menyesuaikan batas pencarian calon IP agar target Anda tercapai!*

### Opsi B: Langsung Lewat Baris Perintah (CLI)
Gunakan flag `--target` (jumlah proxy hidup yang diinginkan) dan `--max` (maksimal calon yang dites):

* **Mau 50 Proxy Hidup:**
  ```powershell
  python main.py --target 50 --max 800
  ```
* **Mau 100 Proxy Hidup:**
  ```powershell
  python main.py --target 100 --max 1500
  ```
* **Mau 25 Proxy Khusus SOCKS5:**
  ```powershell
  python main.py --protocol socks5 --target 25 --max 500
  ```

---

## 3. Cara Menjalankan Local Rotating Proxy & REST API (Port 8888)

Fitur ini membuat komputer Anda menjadi **Proxy Gateway Lokal**. Anda tidak perlu repot gonta-ganti IP di bot Anda. Cukup arahkan bot ke `127.0.0.1:8888`, dan OmniProxy yang akan merotasi request ke proxy-proxy hidup secara otomatis!

### Menjalankan Server:
```powershell
python main.py --serve 8888 --target 20
```

### Mengakses REST API (Bisa dibuka di Browser):
* **`http://127.0.0.1:8888/api/random`** : Mengambil 1 proxy hidup tercepat secara acak (JSON).
* **`http://127.0.0.1:8888/api/all`** : Mengambil semua proxy yang aktif di memori (JSON).
* **`http://127.0.0.1:8888/api/status`** : Melihat uptime, total request yang sudah dirotasi, dan kesehatan pool.

### Menguji Forward Proxy lewat Terminal / cURL:
```powershell
curl.exe -x http://127.0.0.1:8888 https://api.ipify.org
```

---

## 4. Cara Panen Khusus Proxy Tertentu

### A. Khusus Proxy Elite (High Anonymous)
Proxy tipe ini 100% menyembunyikan identitas Anda dan tidak meninggalkan header proxy apa pun:
```powershell
python main.py --anonymity elite --target 20
```
*Hasil otomatis tersimpan khusus di `output/live_elite.txt`.*

### B. Khusus Negara Tertentu (ID, SG, US, dll)
* **Khusus Indonesia (ID):**
  ```powershell
  python main.py --country ID --target 10
  ```
* **Khusus Singapura (SG):**
  ```powershell
  python main.py --country SG --target 15
  ```
* **Khusus Amerika Serikat (US):**
  ```powershell
  python main.py --country US --target 20
  ```

### C. Khusus Tembus Website Tertentu (Google, Shopee, dll)
Untuk memastikan proxy tidak diblokir atau kena CAPTCHA oleh website target:
* **Tes Tembus Google:**
  ```powershell
  python main.py --target-url https://google.com --target 10
  ```
* **Tes Tembus Marketplace:**
  ```powershell
  python main.py --target-url https://shopee.co.id --target 10
  ```

---

## 5. Cara Integrasi ke Script Python / Scraper / Bot

### Contoh 1: Menggunakan Local Rotating Gateway (Paling Direkomendasikan)
Setelah menjalankan `python main.py --serve 8888`, bot Python Anda cukup disetting seperti ini:

```python
import requests

# Cukup arahkan ke port lokal 8888
proxies = {
    "http": "http://127.0.0.1:8888",
    "https": "http://127.0.0.1:8888"
}

# Setiap request otomatis berganti IP dari pool yang hidup!
for i in range(5):
    resp = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10)
    print(f"Request #{i+1} menggunakan IP:", resp.json()["ip"])
```

### Contoh 2: Mengambil IP dari REST API secara Dinamis
```python
import requests

# Ambil 1 proxy acak dari OmniProxy API
api_resp = requests.get("http://127.0.0.1:8888/api/random").json()
proxy_url = api_resp["url"]
print(f"Menggunakan proxy: {proxy_url} ({api_resp['country']} - {api_resp['anonymity']})")

# Gunakan proxy tersebut untuk scraping
data = requests.get("https://api.ipify.org", proxies={"http": proxy_url, "https": proxy_url})
print("IP Aktif:", data.text)
```

### Contoh 3: Membaca File Hasil Panen Langsung
File hasil panen selalu diperbarui di folder `output/`:
- `output/live_all.txt` : Format `IP:Port`
- `output/live_urls.txt` : Format `http://IP:Port` atau `socks5://IP:Port`
- `output/live_elite.txt` : Format URL khusus proxy Elite

```python
with open("output/live_all.txt", "r") as f:
    proxy_list = [line.strip() for line in f if line.strip()]

print(f"Ada {len(proxy_list)} proxy siap pakai!")
```

---

## 6. Tabel Semua Perintah CLI Lengkap

| Perintah | Fungsi |
| :--- | :--- |
| `python main.py` | Membuka TUI Menu Interaktif bergaya kotak |
| `python main.py --target 50` | Panen 50 proxy hidup tercepat |
| `python main.py --protocol socks5 --target 20` | Panen 20 proxy khusus SOCKS5 |
| `python main.py --country ID --target 10` | Panen 10 proxy khusus lokasi Indonesia |
| `python main.py --anonymity elite --target 15` | Panen 15 proxy tingkat Elite (Anti Bocor) |
| `python main.py --target-url https://google.com` | Validasi proxy langsung ke target web |
| `python main.py --serve 8888 --target 20` | Jalankan Rotating Forward Proxy & REST API di port 8888 |
| `python main.py --loop 15 --target 30` | Auto-refresh panen otomatis tiap 15 menit |
| `python main.py --sync-9router auto` | Sinkronisasi proxy otomatis ke 9Router SQLite |

---
*Created & maintained by **@itzluthfi** (https://github.com/itzluthfi)*
