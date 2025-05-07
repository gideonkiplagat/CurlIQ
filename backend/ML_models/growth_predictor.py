import os
import cv2
import numpy as np

def predict_growth(image_path, hair_analysis):
    """
    Predict hair growth based on image and hair health analysis
    
    Args:
        image_path: Path to the image file
        hair_analysis: Dictionary containing:
            - score: Overall health score (0-100)
            - thickness: Hair thickness metric
            - shininess: Shine quality metric
    """
    try:
        # Validate input
        if not isinstance(hair_analysis, dict):
            raise ValueError("hair_analysis must be a dictionary")
            
        if not os.path.exists(image_path):
            raise FileNotFoundError("Image file not found")

        # Get metrics with defaults
        health_score = float(hair_analysis.get('score', 50))
        thickness = float(hair_analysis.get('thickness', 0.5))
        
        # Calculate growth factors
        health_factor = 0.5 + (health_score / 200)
        thickness_factor = 1.2 - (thickness / 1000)
        
        # Base growth rate (inches/month)
        base_rate = 0.5
        adjusted_rate = base_rate * health_factor * thickness_factor
        
        return {
            'monthly_rate_inches': adjusted_rate,
            'six_month_prediction': adjusted_rate * 6,
            'health_factor': health_factor,
            'thickness_factor': thickness_factor
        }
        
    except Exception as e:
        print(f"Growth prediction error: {e}")
        return {
            'error': 'Growth prediction failed',
            'details': str(e)
        }
