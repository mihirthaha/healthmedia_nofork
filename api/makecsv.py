import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configure headless Chrome browser
options = Options()
options.add_argument("--headless=new")
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)

# List of Instagram post/reel URLs
reel_urls = [
    "https://www.instagram.com/legolandcalifornia/reel/DI1xRs8TWJX/?hl=en",
    "https://www.instagram.com/legolandcalifornia/p/DHoIiYTO042/?hl=en",
    "https://www.instagram.com/legolandcalifornia/reel/DIzd68Svk5b/?hl=en",
    "https://www.instagram.com/legolandcalifornia/reel/DIw4DwHOSBI/?hl=en",
    "https://www.instagram.com/legolandcalifornia/reel/DIwuzRCzP6C/?hl=en",
    "https://www.instagram.com/legolandcalifornia/reel/DItfPIlqMQO/?hl=en",
    "https://www.instagram.com/legolandcalifornia/reel/DIo7jRDz5bW/?hl=en",
    "https://www.instagram.com/legolandcalifornia/reel/DIkXhHoTULo/?hl=en",
    "https://www.instagram.com/legolandcalifornia/reel/DIj9QuMTGAI/?hl=en",
    "https://www.instagram.com/legolandcalifornia/p/DIhYFlqzC3A/?hl=en",
    "https://www.instagram.com/legolandcalifornia/reel/DIe_egUzt42/?hl=en",
    "https://www.instagram.com/legolandcalifornia/p/DICkUZ6BbiM/?hl=en",
    "https://www.instagram.com/legolandcalifornia/reel/DJFWe1kTUPb/?hl=en",
    "https://www.instagram.com/legolandcalifornia/p/DIhYFlqzC3A/",
    "https://www.instagram.com/legolandcalifornia/reel/DIj9QuMTGAI/",
    "https://www.instagram.com/legolandcalifornia/reel/DIe_egUzt42/",
    
]

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

        return {
            "url": url,
            "likes/views": likes_or_views,
            "time_of_day": time_of_day
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {
            "url": url,
            "likes/views": "Error",
            "time_of_day": "Error"
        }

# Scrape each post and collect results
results = []
for url in reel_urls:
    print(f"Scraping: {url}")
    data = process_instagram_post(url)
    results.append(data)

# Write results to CSV
with open("legoland_posts.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["url", "likes/views", "time_of_day"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in results:
        writer.writerow(row)

print("✅ CSV created: legoland_posts.csv")
driver.quit()
