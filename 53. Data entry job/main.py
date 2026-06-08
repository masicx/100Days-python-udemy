import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdIbC0-pYIS7fQQzHn0RGuQKsWMl4fdsSK5VT7ZSPa7NndJzA/viewform?usp=publish-editor"
ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(ZILLOW_CLONE_URL)
zillow_web_page = response.text

soup = BeautifulSoup(zillow_web_page, "html.parser")
all_sites = soup.find_all(name="div", class_="StyledPropertyCardDataWrapper")

driver = webdriver.Edge()

for site in all_sites:
    driver.get(FORM_URL)
    time.sleep(1)
    price = site.find(name="span", class_="PropertyCardWrapper__StyledPriceLine").getText().split("+")[0]
    address = site.find(name="address").getText().strip()
    link = site.find(name="a", class_="StyledPropertyCardDataArea-anchor")["href"]

    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(address)
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(price)
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(link)

    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()