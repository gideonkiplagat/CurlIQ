import sys
import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5500"])


sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.services.storage_services import save_uploaded_image
from backend.ML_models.face_shape import FaceShapeAnalyzer
from backend.ML_models.hair_health import analyze_hair_health
from backend.ML_models.growth_predictor import predict_growth
from backend.services.salon_services import find_recommended_salons

app = Flask(__name__)
face_analyzer = FaceShapeAnalyzer()

@app.route('/favicon.ico')
def favicon():
    return '', 404

@app.route('/')
def home():
    return "Haircut Recommendation API is running!"

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save image
        image_path = save_uploaded_image(image)
        if not os.path.exists(image_path):
            raise ValueError("Failed to save image")

        # Analyze face shape
        face_shape = face_analyzer.analyze_face_shape(image_path)
        if not face_shape:
            raise ValueError("Could not detect face or determine shape")

        # Analyze hair health
        hair_health = analyze_hair_health(image_path)
        if not hair_health:
            raise ValueError("Hair health analysis failed")

        # Predict growth
        growth_prediction = predict_growth(
            image_path=image_path,
            hair_analysis=hair_health
        )

        # Get salon recommendations
        location = request.form.get('location', 'Nairobi')  # Default to Nairobi
        salons = find_recommended_salons(face_shape, location)

        return jsonify({
            'face_shape': face_shape,
            'hair_health': hair_health,
            'growth_prediction': growth_prediction,
            'recommended_salons': salons,
            'recommended_hairstyles': []
        })

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({
            'error': 'Analysis failed',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
