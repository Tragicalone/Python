import os
from selenium import webdriver
from selenium.webdriver.common.by import By

try:
    driver = webdriver.Chrome()
    driver.get('http://24h.pchome.com.tw/region/DHBE')
    driver.maximize_window()
    driver.implicitly_wait(10)

    for ItemIndex, DDTag in enumerate(driver.find_elements(By.XPATH, '//dl[@id="Block12Container50"]/dd')):
        title = DDTag.find_element(By.XPATH, './div/h5/a').text
        price = DDTag.find_element(By.XPATH, './div/ul/li/span/span').text
        if title and price:
            TextTarget(str(ItemIndex) + '  ' + title + ' - ' + price)

except Exception as exp:
    TextTarget(exp)
finally:
    driver.quit()
