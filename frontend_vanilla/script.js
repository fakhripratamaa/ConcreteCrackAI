/**
 * Script for ConcreteCrack AI Vanilla Frontend
 * Interacts with Flask API Backend using Fetch API
 */

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadContent = document.getElementById('uploadContent');
const imagePreview = document.getElementById('imagePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsSection = document.getElementById('resultsSection');

// Results DOM Elements
const resultOriginalImage = document.getElementById('resultOriginalImage');
const resultCvImage = document.getElementById('resultCvImage');
const statusBadge = document.getElementById('statusBadge');
const resConfidence = document.getElementById('resConfidence');
const resOrientation = document.getElementById('resOrientation');
const resCondition = document.getElementById('resCondition');

// Dashboard DOM Elements
const statConfidence = document.getElementById('statConfidence');
const statTime = document.getElementById('statTime');
const statResolution = document.getElementById('statResolution');

let selectedFile = null;

// --- Event Listeners for Drag and Drop ---

// Klik pada area upload untuk membuka file dialog
uploadArea.addEventListener('click', () => fileInput.click());

// Saat gambar diseret ke atas area upload
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

// Saat gambar keluar dari area upload
uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

// Saat gambar dilepaskan di area upload
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    if (e.dataTransfer.files.length > 0) {
        handleFile(e.dataTransfer.files[0]);
    }
});

// Saat file dipilih melalui file input
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

/**
 * Handle dan validasi file yang dipilih
 * @param {File} file 
 */
function handleFile(file) {
    // Validasi format file
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
        alert('Format file tidak didukung! Harap unggah gambar JPG, JPEG, atau PNG.');
        return;
    }

    selectedFile = file;

    // Tampilkan Preview
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
        uploadContent.style.display = 'none';
        
        // Ambil resolusi gambar
        const img = new Image();
        img.onload = function() {
            statResolution.textContent = `${this.width} x ${this.height} px`;
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);

    // Aktifkan tombol analisis
    analyzeBtn.disabled = false;
    
    // Sembunyikan hasil sebelumnya jika ada
    resultsSection.style.display = 'none';
}

// --- Event Listener untuk Tombol Analyze ---
analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    // Tampilkan animasi loading
    analyzeBtn.style.display = 'none';
    loadingIndicator.style.display = 'flex';
    resultsSection.style.display = 'none';

    // Siapkan FormData untuk dikirim via POST
    const formData = new FormData();
    formData.append('image', selectedFile);

    // Hitung waktu mulai
    const startTime = performance.now();

    try {
        // Tentukan URL Backend API (Hugging Face Spaces)
        const API_BASE_URL = 'https://fakhri2-concretecrackai-backend.hf.space';

        // Panggil API Flask
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server API merespons dengan status ${response.status}`);
        }

        const data = await response.json();
        
        // Hitung total waktu deteksi dalam detik
        const endTime = performance.now();
        const detectionTime = ((endTime - startTime) / 1000).toFixed(2); 

        // Tampilkan hasil ke UI
        displayResults(data, detectionTime);
        
    } catch (error) {
        console.error('Error saat menganalisis:', error);
        alert('Gagal melakukan analisis. Pastikan backend Flask CNN sedang berjalan di port 5000.');
    } finally {
        // Kembalikan tombol dan matikan loading spinner
        analyzeBtn.style.display = 'flex';
        loadingIndicator.style.display = 'none';
    }
});

/**
 * Update UI dengan data hasil analisis dari Flask API
 * @param {Object} data 
 * @param {String} detectionTime 
 */
function displayResults(data, detectionTime) {
    // Tampilkan container hasil
    resultsSection.style.display = 'block';
    
    // Scroll mulus ke bawah agar user bisa langsung melihat hasil
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    // 1. Gambar Asli (diambil dari preview browser)
    resultOriginalImage.src = imagePreview.src;

    // 2. Gambar OpenCV (diambil dari base64 response API)
    resultCvImage.src = `data:image/jpeg;base64,${data.image_base64}`;

    // 3. Detail Deteksi
    // Konversi hasil string menjadi boolean logika
    const isCrack = data.prediction.toUpperCase() === 'CRACK';
    
    // Set badge status dan warna
    statusBadge.textContent = isCrack ? 'Crack Detected' : 'No Crack';
    statusBadge.className = `badge ${isCrack ? 'danger' : 'success'}`;
    
    // Set nilai detail lainnya
    resConfidence.textContent = `${data.confidence}%`;
    resOrientation.textContent = data.orientation || 'N/A';
    resCondition.textContent = data.condition || 'N/A';

    // 4. Update Dashboard Statistik
    statConfidence.textContent = `${data.confidence}%`;
    statTime.textContent = `${detectionTime}s`;
}
