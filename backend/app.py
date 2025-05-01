# Main application entry point
from flask import Flask, request, jsonify
from .services.storage_services import save_uploaded_image
from ML_models.face_shape import analyze_face_shape
from ML_models.hair_health import analyze_hair_health
from ML_models.growth_predictor import predict_growth
from .services.storage_services import find_recommended_salons

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the uploaded image
        image_path = save_uploaded_image(image)

        # Analyze the face shape
        face_shape = analyze_face_shape(image_path)

        # Analyze hair health
        hair_health = analyze_hair_health(image_path)

        # Predict hair growth
        growth_prediction = predict_growth(image_path)

        # Find recommended salons based on analysis
        location = request.form.get('location', '')
        recommended_salons = find_recommended_salons(face_shape, location)

        return jsonify({
            'face_shape': face_shape,
            'hair_health': hair_health,
            'growth_prediction': growth_prediction,
            'recommended_salons': recommended_salons,
            'recommended_hairstyles': []  # Placeholder if you plan to implement hairstyle recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
