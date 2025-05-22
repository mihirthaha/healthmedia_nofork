import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

USERNAME = "jeffburner678"
PASSWORD = "1ms1gmab0y"

# Set up Chrome options
options = Options()
options.add_argument("--headless=new")  # Remove this line if you want to see the browser for debugging
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

# === LOGIN TO INSTAGRAM ===
def login_instagram():
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    time.sleep(1)

    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(6)

    # Skip "Save Your Login Info?"
    try:
        not_now_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now_btn.click()
        time.sleep(3)
    except:
        pass

    # Skip "Turn on Notifications"
    try:
        not_now_btn2 = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now_btn2.click()
        time.sleep(3)
    except:
        pass

login_instagram()

# === CONTINUE WITH YOUR SCRAPING ===
driver.get("https://www.instagram.com/legolandcalifornia/")
time.sleep(5)

post_urls = set()
scroll_pause = 2
max_posts = 200
last_height = driver.execute_script("return document.body.scrollHeight")

def try_click_show_more():
    try:
        buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Show more') or contains(text(), 'Load more')]")
        for button in buttons:
            if button.is_displayed():
                button.click()
                time.sleep(2)
                return True
    except (ElementClickInterceptedException, ElementNotInteractableException):
        pass
    return False

while len(post_urls) < max_posts:
    links = driver.find_elements(By.TAG_NAME, 'a')
    for link in links:
        href = link.get_attribute('href')
        if href and ('/p/' in href or '/reel/' in href):
            post_urls.add(href)
        if len(post_urls) >= max_posts:
            break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause)
    try_click_show_more()

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

post_urls = list(post_urls)[:max_posts]
print(f"✅ Found {len(post_urls)} post URLs.")

def extract_likes_or_views(driver):
    try:
        return driver.find_element(By.XPATH, "//span[contains(text(), 'likes')]/preceding-sibling::span").text
    except:
        try:
            spans = driver.find_elements(By.CSS_SELECTOR, "span[class*='x']")
            for span in spans:
                text = span.text.replace(",", "")
                if text.isdigit() and int(text) > 50:
                    return span.text
        except:
            pass
    return "N/A"

def extract_post_time(driver):
    try:
        time_element = driver.find_element(By.TAG_NAME, "time")
        full_time = time_element.get_attribute("datetime")
        if "T" in full_time:
            hour = int(full_time.split("T")[1].split(":")[0])
            return hour
    except:
        pass
    return "N/A"

def process_instagram_post(url):
    try:
        driver.get(url)
        time.sleep(5)

        likes_or_views = extract_likes_or_views(driver)
        time_of_day = extract_post_time(driver)

        if likes_or_views == "N/A" or time_of_day == "N/A":
            print(f"⏭️ Skipping {url} due to missing data.")
            return None

        return {
            "url": url,
            "likes/views": likes_or_views,
            "time_of_day": time_of_day
        }

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

results = []
for url in post_urls:
    print(f"🔍 Scraping: {url}")
    data = process_instagram_post(url)
    if data:
        results.append(data)

with open("legoland_posts.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["url", "likes/views", "time_of_day"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"✅ CSV created: legoland_posts.csv with {len(results)} valid posts")
driver.quit()
