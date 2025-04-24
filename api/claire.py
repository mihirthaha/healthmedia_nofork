from flask import Flask, request, jsonify
import time
import instaloader
import os

app = Flask(__name__)

def load_instaloader_session(username):
    L = instaloader.Instaloader()
    L.load_session_from_file(username)
    return L

def download_images_from_post(L, post_shortcode, download_folder, retries=5):
    for attempt in range(retries):
        try:
            post = instaloader.Post.from_shortcode(L.context, post_shortcode)

            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            image_filename = os.path.join(download_folder, f"{post_shortcode}.jpg")
            L.download_post(post, target=download_folder)

            return image_filename
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(30)
            else:
                return None

@app.route('/download-image', methods=['POST'])
def download_image():
    data = request.get_json()
    username = data.get('username')
    shortcode = data.get('shortcode')
    download_folder = 'downloaded_images'

    if not username or not shortcode:
        return jsonify({'error': 'Missing username or shortcode'}), 400

    try:
        L = load_instaloader_session(username)
        image_filename = download_images_from_post(L, shortcode, download_folder)
        
        if image_filename:
            return jsonify({'message': 'Download successful', 'file': image_filename})
        else:
            return jsonify({'error': 'Download failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
