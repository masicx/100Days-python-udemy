from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge()
driver.get("https://appbrewery.github.io/gym/")

login_button = driver.find_element(By.ID, "login-button")
login_button.click()
driver.implicitly_wait(2)

email_input = driver.find_element(By.ID, "email-input")
email_input.send_keys("student@test.com")
password_input = driver.find_element(By.ID, "password-input")
password_input.send_keys("password123")

submit_button = driver.find_element(By.ID, "submit-button")
submit_button.click()

driver.implicitly_wait(2)
tuesday_exercises_list = driver.find_element(By.CSS_SELECTOR, "[id^='day-group-tue']")
# Get all the exercises for Tuesday at 6pm where id ends with 1800
tuesday_exercise_6pm = tuesday_exercises_list.find_element(By.CSS_SELECTOR, "[id$='1800']")
tuesday_exercise_6pm.find_element(By.TAG_NAME, "button").click()

driver.quit()