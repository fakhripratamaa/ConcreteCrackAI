import json

with open(r'c:\Users\fakhr\Downloads\projek computer vision\deteksi_retak_beton.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if 'cell_type' in cell and cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'contours, _ = cv2.findContours(' in source:
            old_block = """# 1. Median blur untuk menghilangkan tekstur pasir beton (salt & pepper)
median = cv2.medianBlur(gray, 7)

# 2. Adaptive Thresholding dengan nilai C=15 yang sangat ketat untuk membuang noise
thresh = cv2.adaptiveThreshold(
    median, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY_INV, 51, 15
)

# 3. Membersihkan bintik-bintik kecil (noise) dan menyambung retakan
kernel = np.ones((5,5), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)"""
            new_block = """# 1. Blur ringan agar retakan tipis tidak hilang
blur = cv2.GaussianBlur(gray, (5,5), 0)

# 2. Adaptive Thresholding yang lebih seimbang
thresh = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY_INV, 21, 5
)

# 3. Membersihkan bintik-bintik debu kecil
kernel = np.ones((3,3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)"""
            
            new_source = source.replace(old_block, new_block)
            
            # Update the > 150 check to > 20
            new_source = new_source.replace('valid_contours = [c for c in contours if cv2.contourArea(c) > 150]', 'valid_contours = [c for c in contours if cv2.contourArea(c) > 20]')
            
            cell['source'] = [line + '\n' for line in new_source.split('\n')]
            if cell['source'] and cell['source'][-1] == '\n': cell['source'] = cell['source'][:-1]

with open(r'c:\Users\fakhr\Downloads\projek computer vision\deteksi_retak_beton.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print('Notebook updated with Gentle Pro Mode!')
