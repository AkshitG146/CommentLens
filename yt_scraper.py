from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--disable-software-rasterizer")  


data = []


youtube_video_url = input("Enter the YouTube video URL: ")


with webdriver.Chrome(options=chrome_options) as driver:
    
    wait = WebDriverWait(driver, 10)
    driver.get(youtube_video_url)
    
    
    for _ in range(100):  
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(4)  

    
    comment_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text")))

    
    for i, comment_element in enumerate(comment_elements, 1):
        comment_text = comment_element.text
        
        
        try:
            likes_element = comment_element.find_element(By.XPATH, './ancestor::ytd-comment-thread-renderer//span[@id="vote-count-middle"]')
            likes = likes_element.text if likes_element.text else "0"
        except:
            likes = "0"  
        
        
        # try:
        #     replies_element = comment_element.find_element(By.XPATH, './ancestor::ytd-comment-thread-renderer//yt-formatted-string[@id="text" and @class="more-button style-scope ytd-button-renderer"]')
        #     replies = replies_element.text if replies_element.text else "0"
        # except:
        #     replies = "0"  
        
        
        data.append({
            'comment': comment_text,
            'likes': likes,
            #'replies': replies
        })
        
        print(f"Comment {i}: {comment_text} | Likes: {likes} ")


df = pd.DataFrame(data)
print(df.head())

df.to_csv('assets\youtube_comments2.csv', index=False)

