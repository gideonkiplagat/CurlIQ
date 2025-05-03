# # Face shape detection model
# import cv2
# import numpy as np
# import dlib
# import math
# from .. utils.image_utils import get_face_landmarks, get_face_shape, align_face, get_face_shape_name
# from utils.image_utils import resize_image, save_image
# from ..utils.image_utils import align_face
# from ..utils.config import SHAPE_PREDICTOR_PATH

# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# def analyze_face_shape(image_path):
#     """
#     Analyzes the face shape from the provided image path.

#     Args:
#         image_path (str): Path to the image file.

#     Returns:
#         str: Detected face shape.
#     """
#     # Load and preprocess the image
#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError("Image not found or unable to load.")

#     # Detect faces in the image
#     faces = detector(image, 1)
#     if len(faces) == 0:
#         raise ValueError("No faces detected in the image.")

#     # Process each detected face
#     for face in faces:
#         landmarks = predictor(image, face)
#         landmarks = get_face_landmarks(landmarks)

#         # Align the face
#         aligned_face = align_face(image, landmarks)

#         # Resize the aligned face for consistent processing
#         resized_face = resize_image(aligned_face, (256, 256))

#         # Get the face shape name
#         face_shape_name = get_face_shape_name(resized_face)

#         return face_shape_name

# backend/ML_models/face_shape.py
import cv2
import numpy as np
import mediapipe as mp
from ..utils.config import SHAPE_PREDICTOR_PATH

# class FaceShapeAnalyzer:
#     def __init__(self):
#         self.mp_face_mesh = mp.solutions.face_mesh
#         self.face_mesh = self.mp_face_mesh.FaceMesh(
#             static_image_mode=True,
#             max_num_faces=1,
#             refine_landmarks=True,
#             min_detection_confidence=0.5
#         )

#     def analyze_face_shape(self, image_path):
#         image = cv2.imread(str(image_path))
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         results = self.face_mesh.process(image)
        
#         if not results.multi_face_landmarks:
#             raise ValueError("No face detected in the image")
        
#         landmarks = results.multi_face_landmarks[0].landmark
        
#         # Get key points (simplified)
#         left_ear = landmarks[454]  # Approximate
#         right_ear = landmarks[234]
#         chin = landmarks[152]
#         forehead = landmarks[10]
        
#         # Calculate ratios
#         face_width = right_ear.x - left_ear.x
#         face_height = chin.y - forehead.y
#         jaw_width = landmarks[365].x - landmarks[135].x
        
#         # Determine shape
#         ratio = face_height / face_width
        
#         if ratio > 1.3:
#             return "oblong"
#         elif jaw_width/face_width < 0.9:
#             return "heart"
#         elif abs(ratio - 1.0) < 0.1:
#             return "round"
#         else:
#             return "oval"

class FaceShapeAnalyzer:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )

    def analyze_face_shape(self, image_path):
        try:
            # Read and preprocess image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not read image file")
                
            # Convert to RGB and get dimensions
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w = image.shape[:2]
            
            # Process with explicit dimensions
            results = self.face_mesh.process(image)
            
            if not results.multi_face_landmarks:
                return None
                
            # Get landmarks and calculate ratios
            landmarks = results.multi_face_landmarks[0].landmark
            
            # Convert landmarks to pixel coordinates
            def landmark_to_pixels(lm):
                return int(lm.x * w), int(lm.y * h)
            
            # Key facial points
            left_ear = landmark_to_pixels(landmarks[454])
            right_ear = landmark_to_pixels(landmarks[234])
            chin = landmark_to_pixels(landmarks[152])
            forehead = landmark_to_pixels(landmarks[10])
            
            # Calculate face metrics
            face_width = right_ear[0] - left_ear[0]
            face_height = chin[1] - forehead[1]
            jaw_width = landmark_to_pixels(landmarks[365])[0] - landmark_to_pixels(landmarks[135])[0]
            
            # Determine shape
            ratio = face_height / face_width
            
            if ratio > 1.3:
                return "oblong"
            elif jaw_width/face_width < 0.9:
                return "heart"
            elif abs(ratio - 1.0) < 0.1:
                return "round"
            else:
                return "oval"
                
        except Exception as e:
            print(f"Face shape analysis error: {e}")
            return None
