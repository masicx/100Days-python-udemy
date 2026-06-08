from selenium import webdriver
from selenium.webdriver.common.by import By

edge_options = webdriver.EdgeOptions()
# edge_options.add_experimental_option("detach", True) # Not working for Edge
driver = webdriver.Edge(options=edge_options)
# driver.get("https://www.amazon.com.mx/vantisan-Inteligente-Inal%C3%A1mbrico-Recargable-Bidireccional/dp/B0DRYGMBDJ?__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3EXIC7F1SVF07&dib=eyJ2IjoiMSJ9.eq_0mxEv7BMrEYmToze1pIGujmKDrILnxMK5ElN4ACoAjO0c2Y_ZA8d2wnQXCLcf4ErSyV66RJqYhcQxuwf_YqsDTtBE8vomkTFTWX5iP3dAdF1fsBdfwC2gKbWgdEiIPGkm6gIsA_PEu77GVfMKCdh16JP2tm9EwW2LnOsxYZFazMINgFza3eNiu8dN2XFP7wrWpX4TzivsnEMl8y8g9_B73ERLsME4hTPe7pNY-3R7LON6-izL8vrAITVu59Kuvc7LqKQIAndzry50liqqZq9z9ZrYIi2zrL90OfVEW0M.0JMI7pHhiIBGKm4QmoPlscBlctLz_ggaXSf1BKeeqLE&dib_tag=se&keywords=timbre%2Binteligente&qid=1780522498&sprefix=timbre%2Binteligente%2Caps%2C185&sr=8-8&ufe=app_do%3Aamzn1.fos.db4f1a57-87f1-43c5-9a39-0cdca6036b57&th=1")

# continue_ = driver.find_element(By.CLASS_NAME, "a-button-text")
# continue_.click()

# price_element = driver.find_element(By.CLASS_NAME, "a-price")
# price = price_element.text
# print(f"El precio del producto es: {price}")

driver.get("https://www.python.org/")
li_elements = driver.find_elements(By.XPATH, '//*[@id="content"]/div/section/div[2]/div[2]/div/ul/li')

result = {}
for n in range(len(li_elements)):
    time_element = li_elements[n].find_element(By.TAG_NAME, "time")
    a_element = li_elements[n].find_element(By.TAG_NAME, "a")
    result[n] = { "time": time_element.text, "name": a_element.text}
    
print(result)
driver.quit()