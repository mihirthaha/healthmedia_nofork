import time
import instaloader

# seting commit
# Load session using the Instagram username (Instaloader finds the correct file)
def load_instaloader_session(username):
    L = instaloader.Instaloader()
    L.load_session_from_file(username)
    return L

# Fetch comments for a post, including pagination
def fetch_comments_with_pagination(L, post_shortcode, retries=5):
    comments = []
    for attempt in range(retries):
        try:
            post = instaloader.Post.from_shortcode(L.context, post_shortcode)
            for comment in post.get_comments():
                comments.append(comment.text)
            print(f"Successfully fetched {len(comments)} comments for post {post_shortcode}")
            return comments
        except Exception as e:
            print(f"Error fetching comments for {post_shortcode}: {e}")
            if attempt < retries - 1:
                wait_time = 30
                print(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print("Max retries reached. Skipping this post.")
                return None

# Main execution
def main():
    username = 'hahahahaht1'  # Your actual Instagram username tied to the session
    post_shortcodes = ['DIKdb7Gy5vM', 'DIE6HE2B_nK']  # Replace with real post shortcodes if needed

    L = load_instaloader_session(username)

    for shortcode in post_shortcodes:
        print(f"Processing post: {shortcode}")
        comments = fetch_comments_with_pagination(L, shortcode)

        if comments:
            print(f"\nComments for {shortcode}:")
            for c in comments:
                print("-", c)
        else:
            print(f"Failed to fetch comments for post {shortcode}.")

        time.sleep(10)

if __name__ == "__main__":
    main()
