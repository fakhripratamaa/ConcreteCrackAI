import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model_path = r"C:\Users\fakhr\Downloads\projek computer vision\best_crack_model.keras"
model = load_model(model_path)

# Mencari file jpg apa saja di folder ini
for f in os.listdir(r"C:\Users\fakhr\Downloads\projek computer vision"):
    if f.lower().endswith('.jpg'):
        img_path = os.path.join(r"C:\Users\fakhr\Downloads\projek computer vision", f)
        img = image.load_img(img_path, target_size=(227, 227))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        
        pred = model.predict(img_array)[0][0]
        print(f"File: {f} | Score: {pred}")
