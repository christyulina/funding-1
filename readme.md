# 💰 Dashboard Monitoring Deposito Bulanan

Aplikasi ini dibuat dengan **Streamlit** untuk membantu monitoring deposito dan bunga yang diterima dari berbagai bank setiap bulan. Data bersumber dari file Excel yang diunggah oleh pengguna.

---

## 🚀 Fitur Aplikasi

- 📈 Line chart: Total bunga deposito per bulan
- 📊 Bar chart: Total nominal deposito per bulan
- 🥧 Pie chart: Distribusi deposito per bank
- 📘 Line chart: Bunga deposito per bulan untuk bank **Buku IV** (BRI, Mandiri, BNI)
- 📙 Line chart: Bunga deposito per bulan untuk bank **Buku III** (BTN, BSI, BTN Syariah)
- 📋 Tabel ringkasan data

---

## 📁 Format File Excel

| Tanggal     | Bank         | Nominal     | Bunga       |
|-------------|--------------|-------------|-------------|
| 2025-01-01  | Bank BRI     | 100000000   | 1200000     |
| 2025-01-01  | Bank BTN     | 75000000    | 950000      |

> **Catatan:** Pastikan nama kolom di Excel persis seperti di atas.

---

## 🛠️ Cara Menjalankan Aplikasi Secara Lokal

### 1. Clone repo ini:
```bash
git clone https://github.com/username/deposito-dashboard.git
cd deposito-dashboard
