# salon recommendation storage service
# Mock data - replace with real API calls
SALONS = [
    {'id': 1, 'name': 'Elite Cuts', 'rating': 4.8, 'specialty': ['oval', 'round'], 'location': 'New York'},
    {'id': 2, 'name': 'Precision Barbers', 'rating': 4.6, 'specialty': ['square', 'oblong'], 'location': 'Chicago'},
    {'id': 3, 'name': 'Curly Hair Experts', 'rating': 4.9, 'specialty': ['heart', 'oval'], 'location': 'Los Angeles'}
]

def find_recommended_salons(face_shape, location=None):
    # Filter by face shape specialty
    recommended = [salon for salon in SALONS if face_shape in salon['specialty']]
    
    # If location provided, filter by location
    if location:
        recommended = [salon for salon in recommended if location.lower() in salon['location'].lower()]
    
    # Sort by rating
    recommended.sort(key=lambda x: x['rating'], reverse=True)
    
    return recommended[:5]  # Return top 5 recommended salons