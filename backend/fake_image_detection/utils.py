import numpy as np
import cv2
from scipy.stats import skew, kurtosis
from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy
from PIL import Image
import warnings
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

def analyze_image(image_file):
    try:
        # Step 1: Load and preprocess image
        img = Image.open(image_file).convert('RGB')
        img = img.resize((512, 512))  # Higher resolution for better analysis
        img_gray = img.convert('L')
        
        # Convert to NumPy arrays
        img_array = np.array(img_gray)
        img_rgb = np.array(img)
        
        # Step 2: Enhanced Color Analysis (RGB & HSV)
        img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
        
        color_stats = {}
        for i, channel in enumerate(['r', 'g', 'b']):
            color_stats[f'{channel}_mean'] = np.mean(img_rgb[:, :, i])
            color_stats[f'{channel}_std'] = np.std(img_rgb[:, :, i])
            color_stats[f'{channel}_skew'] = skew(img_rgb[:, :, i].flatten())
        
        for i, channel in enumerate(['h', 's', 'v']):
            color_stats[f'{channel}_mean'] = np.mean(img_hsv[:, :, i])
            color_stats[f'{channel}_std'] = np.std(img_hsv[:, :, i])
        
        # Step 3: Histogram & Entropy Analysis
        hist = cv2.calcHist([img_array], [0], None, [256], [0, 256])
        hist_entropy = shannon_entropy(hist)
        
        # Step 4: Texture Analysis (GLCM)
        distances = [1, 3]
        angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        glcm = graycomatrix(img_array, distances=distances, angles=angles, symmetric=True, normed=True)
        
        texture_features = {
            'contrast': np.mean(graycoprops(glcm, 'contrast')),
            'homogeneity': np.mean(graycoprops(glcm, 'homogeneity')),
            'energy': np.mean(graycoprops(glcm, 'energy')),
            'correlation': np.mean(graycoprops(glcm, 'correlation'))
        }
        
        # Step 5: Sharpness & Edge Analysis
        sharpness_measures = {
            'laplacian_var': cv2.Laplacian(img_array, cv2.CV_64F).var(),
            'sobel_edges': np.mean(cv2.Sobel(img_array, cv2.CV_64F, 1, 1, ksize=3))
        }
        
        # Step 6: Noise Estimation
        denoised = cv2.fastNlMeansDenoising(img_array, None, 10, 7, 21)
        noise = img_array - denoised
        noise_std = np.std(noise)
        
        # Step 7: Frequency Domain Analysis (FFT)
        dft = np.fft.fft2(img_array)
        dft_shift = np.fft.fftshift(dft)
        magnitude_spectrum = 20 * np.log(np.abs(dft_shift))
        freq_std = np.std(magnitude_spectrum)
        
        # Step 8: Feature Weighting & Fake Score Calculation
        # Define expected normal ranges (empirically adjusted)
        feature_ranges = {
            'laplacian_var': (100, 500),  # Sharpness (too low = blurry, too high = artificial)
            'contrast': (50, 300),        # Texture contrast
            'homogeneity': (0.3, 0.8),    # Texture smoothness
            'noise_std': (2, 15),        # Noise level
            'freq_std': (10, 30),        # Frequency patterns
            's_mean': (50, 180),         # Saturation (HSV)
            'v_std': (15, 50),           # Value variation (HSV)
            'hist_entropy': (4, 7),      # Histogram distribution
            'r_std': (20, 60),           # Red channel variation
            'g_std': (20, 60),           # Green channel variation
            'b_std': (20, 60)           # Blue channel variation
        }
        
        # Calculate deviation from expected ranges
        fake_score = 0
        
        # 1. Sharpness check (Laplacian variance)
        if sharpness_measures['laplacian_var'] < 100:
            fake_score += 0.2 * (100 - sharpness_measures['laplacian_var']) / 50
        elif sharpness_measures['laplacian_var'] > 500:
            fake_score += 0.1 * (sharpness_measures['laplacian_var'] - 500) / 100
        
        # 2. Texture check (Contrast & Homogeneity)
        if texture_features['contrast'] < 50:
            fake_score += 0.15 * (50 - texture_features['contrast']) / 10
        if texture_features['homogeneity'] > 0.8:
            fake_score += 0.1 * (texture_features['homogeneity'] - 0.8) * 10
        
        # 3. Noise check
        if noise_std > 15:
            fake_score += 0.15 * min(noise_std / 15, 2)  # Cap at 2x
        
        # 4. Frequency check (FFT)
        if freq_std < 10:
            fake_score += 0.1 * (10 - freq_std) / 2
        
        # 5. Color checks (HSV & RGB)
        if color_stats['s_mean'] < 50 or color_stats['s_mean'] > 180:
            fake_score += 0.05
        if color_stats['v_std'] < 15:
            fake_score += 0.05 * (15 - color_stats['v_std']) / 5
        
        # 6. Histogram check (Entropy)
        if hist_entropy < 4:
            fake_score += 0.05 * (4 - hist_entropy)
        
        # Normalize fake_score to [0, 1]
        fake_score = min(max(fake_score, 0), 1)
        
        # Step 9: Confidence & Decision
        # Sigmoid to convert score to probability (more balanced)
        def sigmoid(x):
            return 1 / (1 + np.exp(-12 * (x - 0.5)))
        
        probability = sigmoid(fake_score)
        confidence = min(max(70 + (probability - 0.5) * 60, 50), 90)  # 50-90% range
        
        # Final decision (threshold at 0.6 probability)
        is_fake = probability > 0.6
        
        return is_fake, round(confidence, 2)
    
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return False, 50.0  # Default to "real" if error occurs
