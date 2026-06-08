from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import platform, time

EMAIL = "masicx@gmail.com"
PASSWORD = "CU9ZB5y-KdmboSVn"
PASTE_KEY = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL

class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Edge()
        self.up = ""
        self.down = ""

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(3)
        go_button = self.driver.find_element(By.CLASS_NAME, "start-text")
        go_button.click()
        time.sleep(60)
        self.up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text
        self.down = self.driver.find_element(By.CLASS_NAME, "download-speed").text

    def tweet_at_provider(self):
        self.driver.get("https://app.100daysofpython.dev/services/y")
        login_button = self.driver.find_element(By.CLASS_NAME, "y-login-link")
        login_button.click()

        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys(EMAIL)
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(PASSWORD)
        login_button = self.driver.find_element(By.CLASS_NAME, "y-login-submit")
        login_button.click()

        tweet_compose = self.driver.find_element(By.ID, "tweet-compose")
        tweet_compose.send_keys("I am so mad at you, 100 Days of Python! Your service is terrible INTERNET SPEED: UP: " + self.up + " DOWN: " + self.down + " and I want a refund!")

        port_btn = self.driver.find_element(By.ID, "post-btn")
        port_btn.click()

bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()

time.sleep(50)
# self.driver.quit()