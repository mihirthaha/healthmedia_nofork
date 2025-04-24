import time
import instaloader
import os
import colorsys
from PIL import Image


# Load session using the Instagram username (Instaloader finds the correct file)
def load_instaloader_session(username):
    L = instaloader.Instaloader()
    L.load_session_from_file(username)
    return L

# Download images from the post
def download_images_from_post(L, post_shortcode, download_folder, retries=5):
    for attempt in range(retries):
        try:
            # Get the post using its shortcode
            post = instaloader.Post.from_shortcode(L.context, post_shortcode)

            # Create the download folder if it doesn't exist
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            # Download the post's main image (first image in the post)
            image_url = post.url  # URL for the main image
            image_filename = os.path.join(download_folder, f"{post_shortcode}.jpg")
            L.download_post(post, target=download_folder)  # This handles downloading the image
            
            print(f"Successfully downloaded image from post {post_shortcode}")
            return image_filename
        except Exception as e:
            print(f"Error downloading image for {post_shortcode}: {e}")
            if attempt < retries - 1:
                wait_time = 30
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print("Max retries reached. Skipping this post.")
                return None

# Main execution
def main():
    username = 'clairelee0817'  # Your actual Instagram username tied to the session
    post_shortcodes = ['DIKdb7Gy5vM', 'DIE6HE2B_nK']  # Replace with real post shortcodes if needed
    download_folder = 'downloaded_images'  # Folder to save images
    L = load_instaloader_session(username)
    
    for shortcode in post_shortcodes:
        print(f"Processing post: {shortcode}")
        image_filename = download_images_from_post(L, shortcode, download_folder)
        
        if image_filename:
            print(f"Image downloaded successfully: {image_filename}")
        else:
            print(f"Failed to download image for post {shortcode}.")
        
        time.sleep(10)  # Small delay between requests to avoid rate limiting

if __name__ == "__main__":
    main()
    
def extract_saturation_brightness(image_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    num_pixels = width * height
    pixels = list(img.getdata())
    saturations = []
    brightnesses = []
    for r, g, b in pixels:
        r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
        _, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
        saturations.append(s)
        brightnesses.append(v)
    avg_saturation = sum(saturations) / num_pixels
    avg_brightness = sum(brightnesses) / num_pixels
    return saturations, brightnesses, num_pixels, avg_saturation, avg_brightness

