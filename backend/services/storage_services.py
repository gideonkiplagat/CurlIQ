# Image handling
import os
import os
from werkzeug.utils import secure_filename
from ..utils.config import UPLOAD_FOLDER  # Updated import path
from werkzeug.utils import secure_filename
from ..utils.config import UPLOAD_FOLDER

def save_uploaded_image(file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return filepath




#backend/utils/config.py
# Configuration file for the application
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')   
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
#backend/utils/image_utils.py