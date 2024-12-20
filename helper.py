from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob
import pandas as pd
import time

# Set up the Chrome driver
def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Scroll and load comments
def scroll_and_load_comments(driver, url, scroll_times=50, wait_time=4):
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    for _ in range(scroll_times):
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(wait_time)

# Extract comments and likes
def extract_comments(driver):
    wait = WebDriverWait(driver, 10)
    comment_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text")))
    comments_data = []

    for comment_element in comment_elements:
        comment_text = comment_element.text
        try:
            likes_element = comment_element.find_element(By.XPATH, './ancestor::ytd-comment-thread-renderer//span[@id="vote-count-middle"]')
            likes = likes_element.text if likes_element.text else "0"
        except:
            likes = "0"
        
        comments_data.append({
            'comment': comment_text,
            'likes': likes
        })

    return comments_data

# Main function to scrape YouTube comments
def scrape_comments(video_id, scroll_times=50):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    driver = setup_chrome_driver()
    try:
        scroll_and_load_comments(driver, video_url, scroll_times)
        comments_data = extract_comments(driver)
        return comments_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    finally:
        driver.quit()

# Analyze sentiments
def analyze_sentiments(comments):
    analysis_results = []
    for comment in comments:
        blob = TextBlob(comment['comment'])
        polarity = blob.sentiment.polarity
        sentiment = 'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'
        analysis_results.append({
            'comment': comment['comment'],
            'likes': comment['likes'],
            'sentiment': sentiment,
            'polarity': polarity
        })
    return analysis_results



