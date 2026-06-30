# Menggunakan image Python resmi yang ringan (versi 3.10)
FROM python:3.10-slim

# Hugging Face Spaces sangat menyarankan penggunaan user non-root untuk keamanan
RUN useradd -m -u 1000 user

# Mengatur direktori kerja di dalam container langsung ke folder flask_api
WORKDIR /app/flask_api

# Menyalin file requirements.txt
COPY --chown=user:user flask_api/requirements.txt /app/flask_api/

# Menginstal dependensi Python
# Kita sudah menggunakan tensorflow-cpu dan opencv-python-headless di requirements.txt, 
# sehingga tidak butuh install library OS tambahan.
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode backend
COPY --chown=user:user flask_api/ /app/flask_api/

# Berpindah ke user non-root
USER user

# Hugging Face Spaces MEWAJIBKAN aplikasi mendengarkan pada port 7860
EXPOSE 7860
ENV PORT=7860

# Menjalankan aplikasi menggunakan Gunicorn dengan timeout yang lebih panjang 
# karena inisialisasi model TensorFlow butuh waktu beberapa detik.
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app", "--timeout", "120"]
