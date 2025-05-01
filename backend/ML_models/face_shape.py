# Face shape detection model
import cv2
import numpy as np
import dlib
import math
from .. utils.image_utils import get_face_landmarks, get_face_shape, align_face, get_face_shape_name
from utils.image_utils import resize_image, save_image
from ..utils.image_utils import align_face
from ..utils.config import SHAPE_PREDICTOR_PATH

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def analyze_face_shape(image_path):
    """
    Analyzes the face shape from the provided image path.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Detected face shape.
    """
    # Load and preprocess the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")

    # Detect faces in the image
    faces = detector(image, 1)
    if len(faces) == 0:
        raise ValueError("No faces detected in the image.")

    # Process each detected face
    for face in faces:
        landmarks = predictor(image, face)
        landmarks = get_face_landmarks(landmarks)

        # Align the face
        aligned_face = align_face(image, landmarks)

        # Resize the aligned face for consistent processing
        resized_face = resize_image(aligned_face, (256, 256))

        # Get the face shape name
        face_shape_name = get_face_shape_name(resized_face)

        return face_shape_name
    