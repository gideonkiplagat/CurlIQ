# backend/utils/image_utils.py
import cv2
import numpy as np
import dlib
from pathlib import Path
from ..utils.config import IMAGE_UPLOAD_FOLDER, SHAPE_PREDICTOR_PATH

def align_face(image_path):
    """
    Aligns face using facial landmarks
    Returns aligned face image
    """
    try:
        # Load image
        image = cv2.imread(str(image_path))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Initialize dlib face detector and landmark predictor
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(str(SHAPE_PREDICTOR_PATH))
        
        # Detect faces
        faces = detector(gray)
        if not faces:
            return None
            
        # Get landmarks
        landmarks = predictor(gray, faces[0])
        
        # Calculate alignment angle (simplified)
        left_eye = (landmarks.part(36).x, landmarks.part(36).y)
        right_eye = (landmarks.part(45).x, landmarks.part(45).y)
        
        # Calculate angle between the eyes
        dY = right_eye[1] - left_eye[1]
        dX = right_eye[0] - left_eye[0]
        angle = np.degrees(np.arctan2(dY, dX)) - 180
        
        # Rotate image
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        aligned = cv2.warpAffine(image, M, (w, h), 
                          flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)
        
        return aligned
        
    except Exception as e:
        print(f"Alignment error: {e}")
        return None

def save_temp_image(file):
    """Saves uploaded file to temp location"""
    temp_path = IMAGE_UPLOAD_FOLDER / "temp_upload.jpg"
    with open(temp_path, "wb") as buffer:
        buffer.write(file.read())
    return temp_path
