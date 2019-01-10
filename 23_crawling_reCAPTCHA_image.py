import os
import time
import hashlib
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#不能跑

OutputPath = os.path.abspath('..\PythonResults')
if not os.path.exists(OutputPath):
    os.makedirs(OutputPath)

try:
    ChromeDriver = webdriver.Chrome()
    ChromeDriver.get('https://www.google.com/recaptcha')
    ChromeDriver.maximize_window()
    ChromeDriver.implicitly_wait(10)

    for i in range(5):
        # get image
        ImgURL = ChromeDriver.find_element(
            By.XPATH, '//div[@id="recaptcha_image"]/img').get_attribute('src')

        img_resp = requests.get(ImgURL, stream=True)
        ImageStream = Image.open(img_resp.raw)
        ImgFilename = os.path.join(
            OutputPath, hashlib.md5(ImgURL.encode('utf-8')).hexdigest() + '.' + ImageStream.format)
        ImageStream.save(ImgFilename)
        print('Save img - ', ImgFilename)

        RefreshButton = ChromeDriver.find_element(
            By.XPATH, '//*[@id="recaptcha_reload_btn"]')
        RefreshButton.click()
        time.sleep(2)

except Exception as exp:
    print('Execution Error: ', exp)
finally:
    ChromeDriver.quit()
