import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_channel_videos(channel_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(channel_url)

    try:
        time.sleep(5)
        accept_button_selector = "//button[.//span[text()='Accept all']]"
        reject_button_selector = "//button[.//span[text()='Reject all']]"

        try:
            reject_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, reject_button_selector))
            )
            reject_button.click()
            time.sleep(5)  
        except:
            print("Cookie consent page not found or button not located. Maybe already accepted or N/A.")

        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        for _ in range(3):  
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(5)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        page_source = driver.page_source

    finally:
        driver.quit()

    #  Find video links 
    pattern = re.compile(r'href="(/watch\?v=[^"]+)"')
    matches = pattern.findall(page_source)
    video_urls = { "https://www.youtube.com" + href for href in matches }

    return list(video_urls)