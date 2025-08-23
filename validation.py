import os
import cv2
# import numpy as np
from PIL import Image, UnidentifiedImageError

def validate_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError("Image file not found at given path")

    try:
        # corruption check
        with Image.open(image_path) as img:
            img.verify()

        # reload with cv2
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("Invalid image file format or unreadable image")

        # --- Resolution Check ---
        h, w = img.shape
        # print(f"[DEBUG] Resolution: {w}x{h}")
        # if h < 800 or w < 800:
        #     raise ValueError("Image resolution too low. Please upload a clear image")

        # --- Blur Detection (Laplacian Variance) ---
        variance = cv2.Laplacian(img, cv2.CV_64F).var()
        # print(f"[DEBUG] Blur Variance: {variance}")
        if variance < 500:   # Higher threshold for clarity
            raise ValueError("Image too blurry. Please upload a clear image")

        # --- Aspect Ratio Check ---
        aspect_ratio = w / h
        # print(f"[DEBUG] Aspect Ratio: {aspect_ratio:.2f}")
        # if aspect_ratio < 0.7 or aspect_ratio > 1.6:
        #     raise ValueError("Image looks cropped/tilted. Please upload a proper full invoice image")

    except UnidentifiedImageError:
        raise ValueError("Invalid image file format or unreadable image")

    except Exception as e:
        raise ValueError(f"Image validation failed: {str(e)}")
