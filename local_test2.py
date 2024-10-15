import time

from selenium import webdriver
from selenium.webdriver.chrome import service

from selenium.webdriver.common.by import By

webdriver_service = service.Service(r"C:\\Users\\matte\\AppData\\Local\\Programs\\Opera GX\\operadriver_win64\\operadriver.exe")
webdriver_service.start()

options = webdriver.ChromeOptions()
options.binary_location = "C:\\Users\\matte\\AppData\\Local\\Programs\\Opera GX\\opera.exe"
options.add_experimental_option('w3c', True)

driver = webdriver.Remote(webdriver_service.service_url, options=options)

driver.get('https://www.google.com/')
time.sleep(2)
input_txt = driver.find_element(By.NAME, 'q')
input_txt.send_keys('operadriver\n')

time.sleep(5)  # see the result
driver.quit()