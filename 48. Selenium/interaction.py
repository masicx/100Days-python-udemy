from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Edge()
# driver.get("https://www.wikipedia.org/")

# search = driver.find_element(By.NAME, "search")
# search.send_keys("Python")
# search.submit()

# driver.get("https://appbrewery.github.io/fake-newsletter-signup/")
# first_name = driver.find_element(By.NAME, "fName")
# first_name.send_keys("John")
# last_name = driver.find_element(By.NAME, "lName")
# last_name.send_keys("Doe")
# email = driver.find_element(By.NAME, "email")
# email.send_keys("LH2yj@example.com")
# submit = driver.find_element(By.XPATH, '//*[@id="signup-form"]/button')
# submit.click()

driver.get("https://ozh.github.io/cookieclicker/")
time.sleep(2)
lang = driver.find_element(By.ID, "langSelect-ES")
lang.click()
time.sleep(2)
cookie = driver.find_element(By.ID, "bigCookie")
for n in range(100000):
    cookie.click()
    if n == 12000:
       driver.find_element(By.ID, "product3").click()
    if n == 24000:
        time.sleep(2)


time.sleep(5)
driver.quit()