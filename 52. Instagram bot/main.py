from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

USER_EMAIL = "masicx@gmail.com"
USER_PASSWORD = "zXUZhU4GgGLAl09s"
TARGET_ACCOUNT = ["chefsteps", "rordongamsay", "elaineducasse"]

driver = webdriver.Edge()
driver.get("https://app.100daysofpython.dev/services/share-a-naan/welcome")

email = driver.find_element(By.NAME, "username")
email.send_keys(USER_EMAIL)
password = driver.find_element(By.NAME, "password")
password.send_keys(USER_PASSWORD)
password.send_keys(Keys.ENTER)

for account in TARGET_ACCOUNT:
    driver.get(f"https://app.100daysofpython.dev/services/share-a-naan/u/{account}/")
    followers = driver.find_element(By.CLASS_NAME, "naan-followers-link")
    followers.click()

    # scroll to the bottom of the page to load all followers
    scrollable_div = driver.find_element(By.CLASS_NAME, "followers-scroll")
    last_height = driver.execute_script("return arguments[0].scrollBy(0, arguments[0].scrollHeight);", scrollable_div)
    time.sleep(1)
    follow_buttons = driver.find_elements(By.CLASS_NAME, "naan-follower-row")
    for button in follow_buttons:
        try:
            button.find_element(By.CLASS_NAME, "is-following")
        except NoSuchElementException:
            button.find_element(By.TAG_NAME, "button").click()

driver.quit()
    