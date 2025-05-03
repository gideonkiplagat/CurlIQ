# # backend/utils/config.py
# import os
# from pathlib import Path

# # Base directory setup
# BASE_DIR = Path(__file__).resolve().parent.parent  # Points to backend/

# # Model paths
# MODELS_DIR = BASE_DIR / "ML_models"
# SHAPE_PREDICTOR_PATH = MODELS_DIR / "shape_predictor_68_face_landmarks.dat"

# # Image processing settings
# IMAGE_UPLOAD_FOLDER = BASE_DIR / "uploads"
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# # Ensure directories exist
# IMAGE_UPLOAD_FOLDER.mkdir(exist_ok=True)
# MODELS_DIR.mkdir(exist_ok=True) # Ensure models directory exists


# backend/utils/config.py
import os
from pathlib import Path

# Base directory (points to backend/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Model paths
MODELS_DIR = BASE_DIR / "ML_models"
SHAPE_PREDICTOR_PATH = MODELS_DIR / "shape_predictor_68_face_landmarks.dat"

# Image processing
IMAGE_UPLOAD_FOLDER = BASE_DIR / "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Ensure directories exist
IMAGE_UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
