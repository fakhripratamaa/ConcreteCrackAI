import os
import cv2
import numpy as np
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
CORS(app)

# Load the trained model
from huggingface_hub import hf_hub_download

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_crack_model.keras")
model = None

try:
    # Jika model tidak ada di lokal (misal saat di Docker HF Spaces), download dari HF Model Hub
    if not os.path.exists(MODEL_PATH):
        print("Downloading model from Hugging Face Hub...")
        MODEL_PATH = hf_hub_download(repo_id="fakhri2/ConcreteCrackAI-Model", filename="best_crack_model.keras")
        
    model = load_model(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "ConcreteCrack AI Backend is Online!", "model_loaded": model is not None}), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
        
    file = request.files['image']
    
    # Save temporarily
    temp_path = "temp_img.jpg"
    file.save(temp_path)
    
    try:
        # 1. Prediction using CNN
        img = image.load_img(temp_path, target_size=(227, 227))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        prediction = model.predict(img_array)
        score = float(prediction[0][0])
        
        is_crack = score >= 0.5
        cnn_result = "CRACK" if is_crack else "NO CRACK"
        
        # 2. OpenCV Analysis
        img_cv = cv2.imread(temp_path)
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # 1. Blur ringan agar retakan tipis tidak hilang (Gaussian Blur lebih aman dari Median Blur 7x7)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        
        # 2. Adaptive Thresholding yang lebih seimbang
        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 21, 5
        )
        
        # 3. Membersihkan bintik-bintik debu kecil (dengan kernel 3x3 agar retakan tidak terhapus)
        kernel = np.ones((3,3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        total_area = 0
        total_length = 0
        max_crack_width = 0
        crack_type = "N/A"
        crack_condition = "AMAN"
        
        if contours:
            # Urutkan kontur dari yang terbesar
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            
            # Turunkan batas area menjadi 20 agar retakan tipis tetap terdeteksi
            valid_contours = [c for c in contours if cv2.contourArea(c) > 20]
            
            if valid_contours:
                # Tentukan jenis retakan berdasarkan KONTUR TERBESAR
                largest_contour = valid_contours[0]
                x_l, y_l, w_l, h_l = cv2.boundingRect(largest_contour)
                
                if w_l > h_l * 1.2:
                    crack_type = "HORIZONTAL"
                elif h_l > w_l * 1.2:
                    crack_type = "VERTICAL"
                else:
                    crack_type = "DIAGONAL"
                
                # Hitung statistik dan gambar
                for contour in valid_contours:
                    area = cv2.contourArea(contour)
                    total_area += area
                    
                    x, y, w, h = cv2.boundingRect(contour)
                    crack_width = min(w, h)
                    crack_length = max(w, h)
                    
                    if crack_width > max_crack_width:
                        max_crack_width = crack_width
                    
                    total_length += crack_length
                    
                    # GAMBAR GARIS KONTUR (Lebih elegan, warna hijau mengikuti lekuk retakan)
                    cv2.drawContours(img_rgb, [contour], -1, (0, 255, 0), 2)
                
                # Gambar SATU kotak merah hanya untuk retakan utama (terbesar)
                cv2.rectangle(img_rgb, (x_l, y_l), (x_l + w_l, y_l + h_l), (255,0,0), 3)
        
        if max_crack_width <= 15:
            crack_condition = "RETAKAN KECIL"
        elif max_crack_width <= 35:
            crack_condition = "RETAKAN SEDANG"
        else:
            crack_condition = "RETAKAN LEBAR"
            
        # HYBRID AI + HEURISTIC OVERRIDE:
        if not is_crack and total_area > 100:
            is_crack = True
            cnn_result = "CRACK"
            score = 1.0 - score if score < 0.5 else score
            
        if not is_crack:
            h_img, w_img, _ = img_rgb.shape
            cv2.rectangle(img_rgb, (0, 0), (w_img-1, h_img-1), (0, 255, 0), 10)
            crack_condition = "AMAN"
            crack_type = "N/A"
            
        # Convert analyzed image to base64
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        _, buffer = cv2.imencode('.jpg', img_bgr)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        os.remove(temp_path)
        
        return jsonify({
            'prediction': cnn_result,
            'confidence': round(score * 100, 2),
            'orientation': crack_type,
            'condition': crack_condition,
            'length': total_length,
            'width': max_crack_width,
            'area': total_area,
            'image_base64': img_base64
        })
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
