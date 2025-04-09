import time
import instaloader

# Load session using the Instagram username (Instaloader finds the correct file)
def load_instaloader_session(username):
    L = instaloader.Instaloader()
    L.load_session_from_file(username)
    return L

# Fetch comments for a post, including pagination
def fetch_post_info(L, post_shortcode, retries=5):
    comments = []
    for attempt in range(retries):
        try:
            post = instaloader.Post.from_shortcode(L.context, post_shortcode)

            # Fetch general info
            likes = post.likes
            views = post.video_view_count if post.is_video else 'N/A'
            upload_time = post.date_local.strftime('%Y-%m-%d %H:%M:%S')
            time_of_day = post.date_local.strftime('%p')  # AM or PM

            # Fetch comments
            for comment in post.get_comments():
                comments.append(comment.text)

            print(f"Post {post_shortcode} info:")
            print(f"- Likes: {likes}")
            print(f"- Views: {views}")
            print(f"- Uploaded at: {upload_time} ({time_of_day})")
            print(f"- Total Comments: {len(comments)}\n")

            return {
                "likes": likes,
                "views": views,
                "upload_time": upload_time,
                "time_of_day": time_of_day,
                "comments": comments
            }

        except Exception as e:
            print(f"Error fetching data for {post_shortcode}: {e}")
            if attempt < retries - 1:
                print("Retrying in 30s...")
                time.sleep(30)
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
        post_data = fetch_post_info(L, shortcode)

        if post_data:
            print("Comments:")
            for c in post_data['comments']:
                print("-", c)
        else:
            print(f"Failed to get data for post {shortcode}")

        time.sleep(10)


if __name__ == "__main__":
    main()

