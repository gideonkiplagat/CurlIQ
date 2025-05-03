# backend/app.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from flask import Flask, request, jsonify
from backend.services.storage_services import save_uploaded_image
from backend.ML_models.face_shape import FaceShapeAnalyzer
from backend.ML_models.hair_health import analyze_hair_health
from backend.ML_models.growth_predictor import predict_growth
from backend.services.salon_services import find_recommended_salons  # Fixed filename from salon_services to salon_service

app = Flask(__name__)

# Initialize the face analyzer
face_analyzer = FaceShapeAnalyzer()

@app.route('/')
def home():
    return "Haircut Recommendation API is running!"

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'GET':
        return jsonify({'message': 'Send a POST request with an image file'})
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the uploaded image
        image_path = save_uploaded_image(image)
        
        # Analyze the face shape
        face_shape = face_analyzer.analyze_face_shape(image_path)
        if not face_shape:
            return jsonify({'error': 'Could not detect face or determine face shape'}), 400

        # Analyze hair health
        hair_health = analyze_hair_health(image_path)

        # Predict hair growth
        growth_prediction = predict_growth(image_path)

        # Find recommended salons
        location = request.form.get('location', '')
        recommended_salons = find_recommended_salons(face_shape, location)

        return jsonify({
            'face_shape': face_shape,
            'hair_health': hair_health,
            'growth_prediction': growth_prediction,
            'recommended_salons': recommended_salons,
            'recommended_hairstyles': []
        })

    except Exception as e:
        print(f"Error in /analyze: {str(e)}")  # Log the error for debugging
        return jsonify({'error': 'Image processing failed. Please try another photo.'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    