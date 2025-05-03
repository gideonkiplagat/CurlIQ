
import os
from werkzeug.utils import secure_filename
from backend.utils.config import IMAGE_UPLOAD_FOLDER

import os
from werkzeug.utils import secure_filename
from backend.utils.config import IMAGE_UPLOAD_FOLDER

def save_uploaded_image(file):
    os.makedirs(IMAGE_UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    filepath = os.path.join(IMAGE_UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp'}
           