import numpy as np
import pandas as pd
from PIL import Image
import io
import cv2
from scipy.stats import skew

def analyze_image(image_file):
    # Step 1: Load Image
    img = Image.open(image_file).convert('RGB')
    img = img.resize((256, 256))  # Resize for consistent analysis
    img_gray = img.convert('L')  # Convert to grayscale

    # Step 2: Convert to NumPy array
    img_array = np.array(img_gray)

    # Step 3: Calculate Histogram
    hist = cv2.calcHist([img_array], [0], None, [256], [0,256])
    hist = hist.flatten()

    # Step 4: Calculate Statistics
    mean_val = np.mean(img_array)
    std_dev = np.std(img_array)
    skewness = skew(img_array.flatten())

    # Step 5: Analyze Sharpness (optional but helpful)
    laplacian_var = cv2.Laplacian(img_array, cv2.CV_64F).var()

    # Step 6: Apply Rules for Prediction
    fake_score = 0

    if std_dev < 40 or std_dev > 80:
        fake_score += 1
    if abs(skewness) > 1.5:
        fake_score += 1
    if laplacian_var < 100:  # very smooth images
        fake_score += 1

    # Confidence Calculation
    if fake_score == 0:
        confidence = np.random.uniform(80, 95)
        is_fake = False
    elif fake_score == 1:
        confidence = np.random.uniform(65, 80)
        is_fake = False
    elif fake_score == 2:
        confidence = np.random.uniform(60, 75)
        is_fake = True
    else:
        confidence = np.random.uniform(75, 90)
        is_fake = True

    return is_fake, round(confidence, 2)
