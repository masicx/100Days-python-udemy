from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

APP_URL = "https://app.100daysofpython.dev/services/tindog/u/toU9f07DNFy35t5wwFwoTlfx93GdW1DI"

driver = webdriver.Edge()
driver.get(APP_URL)
login_button = driver.find_element(By.CLASS_NAME, "tindog-nav").find_element(By.TAG_NAME, "button")
login_button.click()
driver.implicitly_wait(1)

login_facebark = driver.find_element(By.CLASS_NAME, "btn-facebark")
login_facebark.click()
driver.implicitly_wait(1)

driver.switch_to.window(driver.window_handles[1])
email_input = driver.find_element(By.ID, "email")
email_input.send_keys("student@test")
password_input = driver.find_element(By.ID, "pass")
password_input.send_keys("password")
login_button = driver.find_element(By.TAG_NAME, "button")
login_button.click()
driver.switch_to.window(driver.window_handles[0])
time.sleep(2)

driver.find_element(By.TAG_NAME, "button").click()
time.sleep(2)
driver.find_element(By.TAG_NAME, "button").click()
time.sleep(2)
driver.find_element(By.TAG_NAME, "button").click()
time.sleep(2)
for _ in range(10):
    try:
        driver.find_element(By.CLASS_NAME, "match-popup").find_element(By.TAG_NAME, "a").click()
    except NoSuchElementException:
        pass
    
    btn_like = driver.find_element(By.CLASS_NAME, "btn-like")
    btn_like.click()

driver.quit()