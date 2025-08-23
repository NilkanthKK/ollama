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



# import cv2
# import numpy as np
# from PIL import Image, UnidentifiedImageError
# import os

# ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}

# def validate_image(image_path, min_width=400, min_height=400, min_variance=100.0):
#     # print(f"Validating image: {image_path}")
#     try:

#         #  Extension check
#         ext = os.path.splitext(image_path)[1].lower().replace(".", "")
#         if ext not in ALLOWED_EXTENSIONS:
#             return False, f" Invalid file type: {ext}"


#         #  Corruption check
#         try:
#             img = Image.open(image_path)
#             img.verify()
#         except UnidentifiedImageError:
#             return False, " File is not a valid image"
#         except Exception as e:
#             return False, f" Image corrupted: {str(e)}"


#         # Reload
#         img = Image.open(image_path)
#         width, height = img.size
#         if width < min_width or height < min_height:
#             return False, f" Too small: {width}x{height}"


#         #  Aspect ratio
#         aspect_ratio = width / height
#         if aspect_ratio < 0.5 or aspect_ratio > 2.0:
#             return False, f" Invalid aspect ratio {aspect_ratio:.2f}"


#         #  Blur check
#         cv_img = cv2.imread(image_path)
#         gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
#         variance = cv2.Laplacian(gray, cv2.CV_64F).var()
#         if variance < min_variance:
#             return False, f" Too blurry (variance={variance:.2f})"


#         #  Edge + contour detection
#         edged = cv2.Canny(gray, 50, 200)
#         contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         if not contours:
#             return False, " No document detected"


#         # Largest contour
#         c = max(contours, key=cv2.contourArea)
#         peri = cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, 0.02 * peri, True)


#         #  Rectangle check (should have 4 sides)
#         if len(approx) != 4:
#             return False, " Document not rectangular → Possibly cropped"


#         #  Coverage ratio check
#         doc_area = cv2.contourArea(c)
#         img_area = width * height
#         coverage_ratio = doc_area / float(img_area)


#         # If document covers less than 50% → cropped
#         if coverage_ratio < 0.5:
#             return False, f" Document too small (coverage={coverage_ratio:.2f})"


#         # If document covers more than 95% → maybe cropped edges
#         if coverage_ratio > 0.95:
#             return False, f" Document edges cut (coverage={coverage_ratio:.2f})"


#         # print(" Image is valid")
#         return True, " Image is valid"


#     except Exception as e:
#         return False, f" Error: {str(e)}"
