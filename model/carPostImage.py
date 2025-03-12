import base64
import os
from werkzeug.utils import secure_filename
from __init__ import app

def carPostImage_base64_decode(post_id, imageName):
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], "carPostImages", f"{post_id}", imageName)
    try:
        with open(img_path, 'rb') as img_file:
            base64_encoded = base64.b64encode(img_file.read()).decode('utf-8')
        return base64_encoded
    except Exception as e:
        print(f'An error occurred while reading the post picture: {str(e)}')
        return None

def carPostImage_base64_upload(base64_image, post_id, imageName):
    try:
        image_data = base64.b64decode(base64_image)
        filename = secure_filename(imageName)
        car_post_dir = os.path.join(app.config['UPLOAD_FOLDER'], "carPostImages", f"{post_id}")
        if not os.path.exists(car_post_dir):
            os.makedirs(car_post_dir)
        file_path = os.path.join(car_post_dir, filename)
        with open(file_path, 'wb') as img_file:
            img_file.write(image_data)
        return filename 
    except Exception as e:
        print (f'An error occurred while updating the post picture: {str(e)}')
        return None