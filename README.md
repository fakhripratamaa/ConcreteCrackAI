# ConcreteCrack AI

ConcreteCrack AI adalah aplikasi deteksi retakan pada permukaan beton berbasis Computer Vision menggunakan model *Convolutional Neural Network* (CNN) dan deteksi tepi *OpenCV*. 

Proyek ini terdiri dari **Frontend** ringan (Vanilla HTML/CSS/JS) dan **Backend** REST API berbasis Flask.

## 🚀 Fitur Utama
- **Deteksi Otomatis:** Mengklasifikasikan gambar permukaan beton apakah terdapat retakan (Crack) atau tidak (No Crack).
- **Analisis Visual OpenCV:** Memberikan visualisasi garis tepi retakan dan menandai retakan terbesar menggunakan bounding box.
- **Perhitungan Metrik:** Memberikan persentase *Confidence* (Tingkat Keyakinan AI), orientasi retakan, dan kondisi keparahan.
- **Ringan & Responsif:** UI Frontend dibuat tanpa framework berat sehingga memuat dengan sangat cepat dan responsif di semua perangkat.

## 📁 Struktur Repositori
Repository ini menggunakan struktur monorepo yang memisahkan frontend dan backend:
- `/frontend_vanilla` : Berisi antarmuka pengguna statis (UI). Siap di-deploy ke Vercel atau GitHub Pages.
- `/flask_api` : Berisi REST API Python, model AI (Keras/TensorFlow), dan script OpenCV. Siap di-deploy ke platform seperti Render.

## 🛠️ Teknologi yang Digunakan
- **Frontend:** HTML5, CSS3, Vanilla JavaScript, FontAwesome
- **Backend:** Python, Flask, Flask-CORS
- **Computer Vision & AI:** TensorFlow/Keras (CNN), OpenCV, NumPy

## 💻 Cara Menjalankan Secara Lokal (Local Development)

### 1. Menjalankan Backend (Flask API)
1. Buka terminal dan masuk ke folder backend:
   ```bash
   cd flask_api
   ```
2. (Opsional) Buat virtual environment dan aktifkan:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate     # Untuk Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan server Flask:
   ```bash
   python app.py
   ```
   *Backend akan berjalan di `http://127.0.0.1:5000`*

### 2. Menjalankan Frontend
Karena frontend murni bersifat statis, Anda hanya perlu menjalankan server lokal sederhana:
1. Buka terminal baru dan masuk ke folder frontend:
   ```bash
   cd frontend_vanilla
   ```
2. Jalankan server Python HTTP:
   ```bash
   python -m http.server 8000
   ```
3. Buka browser dan akses `http://localhost:8000`

---
*Developed by Fakhri Pratama - Computer Vision Final Project 2026*
