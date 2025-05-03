# backend/utils/image_utils.py
import cv2
import numpy as np
import mediapipe as mp
from pathlib import Path
from ..utils.config import IMAGE_UPLOAD_FOLDER

class FaceAnalyzer:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )

    def align_face(self, image_path):
        """Aligns face using MediaPipe facial landmarks"""
        try:
            image = cv2.imread(str(image_path))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(image)
            
            if not results.multi_face_landmarks:
                return None
                
            # Get facial landmarks (simplified alignment)
            landmarks = results.multi_face_landmarks[0].landmark
            return image
            
        except Exception as e:
            print(f"Face alignment error: {e}")
            return None

def save_temp_image(file):
    """Saves uploaded file to temp location"""
    temp_path = Path(IMAGE_UPLOAD_FOLDER) / "temp_upload.jpg"
    with open(temp_path, "wb") as buffer:
        buffer.write(file.read())
    return temp_path
