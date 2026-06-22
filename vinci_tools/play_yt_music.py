import time
import sys
import psutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def close_existing_chrome():
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if proc.info['name'] == 'chrome.exe' and \
               proc.info['cmdline'] and \
               any('AutomationProfile' in arg for arg in proc.info['cmdline']):
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def play_youtube_song(song_name):
    close_existing_chrome()
    
    options = Options()
    #options.add_argument(r"user-data-dir=C:\Users\USER\AppData\Local\Google\Chrome\AutomationProfile")
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.youtube.com")
        wait = WebDriverWait(driver, 15)
        
        search_box = wait.until(EC.element_to_be_clickable((By.NAME, "search_query")))
        search_box.send_keys(song_name)
        search_box.send_keys(Keys.RETURN)
        
        video_element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@id='video-title'])[1]")))
        video_element.click()
        
        print(f"Playing: {song_name} using Chrome")
    except Exception as e:
        print(f"Failed to play music: {e}")

if __name__ == '__main__':
    # Joining all arguments after the script name to handle multi-word song names correctly
    song = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "lofi hip hop"
    play_youtube_song(song)
