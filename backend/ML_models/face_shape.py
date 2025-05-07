import cv2
import numpy as np
import mediapipe as mp

class FaceShapeAnalyzer:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=False,  # ⬅️ CHANGED: disabled iris refinement for simpler landmark model
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

    def analyze_face_shape(self, image_path):
        try:
            # Read and validate image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Failed to read image file")
                
            # Convert to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, _ = image.shape

            # ⬇️ NEW: Resize to square (fixes NORM_RECT warning)
            size = max(h, w)
            padded_image = np.zeros((size, size, 3), dtype=np.uint8)
            padded_image[:h, :w, :] = image
            image = padded_image
            h, w = size, size  # Update dimensions for landmark scaling
            
            print(f"Image shape after padding: {image.shape}")  # Should show (N, N, 3)


            # Process image
            results = self.face_mesh.process(image)
            
            if not results.multi_face_landmarks:
                return None
                
            # Get facial landmarks
            landmarks = results.multi_face_landmarks[0].landmark
            
            # Convert landmarks to pixel coordinates
            def to_pixels(lm):
                return int(lm.x * w), int(lm.y * h)
            
            # Key facial points
            left_ear = to_pixels(landmarks[454])
            right_ear = to_pixels(landmarks[234])
            chin = to_pixels(landmarks[152])
            forehead = to_pixels(landmarks[10])
            
            # Calculate metrics
            face_width = right_ear[0] - left_ear[0]
            face_height = chin[1] - forehead[1]
            jaw_width = to_pixels(landmarks[365])[0] - to_pixels(landmarks[135])[0]
            
            # Determine shape
            ratio = face_height / face_width
            
            if ratio > 1.3:
                return "oblong"
            elif jaw_width / face_width < 0.9:
                return "heart"
            elif abs(ratio - 1.0) < 0.1:
                return "round"
            else:
                return "oval"
                
        except Exception as e:
            print(f"Face shape error: {e}")
            return None
