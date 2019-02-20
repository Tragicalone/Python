import os
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

try:
    CromeDriver = webdriver.Chrome()
    CromeDriver.get('https://google.com')
    CromeDriver.maximize_window()
    CromeDriver.implicitly_wait(10)

    InputSearch = CromeDriver.find_element(By.XPATH, '//input[@title="搜尋"]')
    InputSearch.send_keys(u'人工智慧')
    InputSearch.send_keys(Keys.ENTER)

    for IndexPage in range(2):
        TextTarget('=' * 87, ' Page ', IndexPage)
        for ATag in CromeDriver.find_elements(By.XPATH, '//div[@class="r"]/a'):
            TextTarget('Title: ', ATag.find_element(By.XPATH, 'h3').text)
            TextTarget('Url:   ', ATag.get_attribute('href'))
        NextPageSpan = CromeDriver.find_element(
            By.XPATH, '//*[@id="pnnext"]/span[2]')
        if not NextPageSpan:
            break
        NextPageSpan.click()

except Exception as exp:
    TextTarget('Execution error: ', exp)
finally:
    CromeDriver.quit()
