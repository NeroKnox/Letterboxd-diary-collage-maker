import time
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import re
import urllib.request

service = Service(r"C:\\Tools\\chrome-win64\\chromedriver-win64\\chromedriver.exe")
options = webdriver.ChromeOptions()
#options.binary_location = "C:\\Tools\\chrome-win64\\chrome.exe"
#options.add_argument('headless')
#options.add_extension('C:\\Users\\matte\\Desktop\\pirateboxd\\AdBlock.crx')
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(600)
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'MyApp/1.0')]
urllib.request.install_opener(opener)
driver.implicitly_wait(5)

link = 'film/the-invisible-man-2020/'
driver.get('https://letterboxd.com/'+ link)

is_foreign = True

try:
    #Click Consent Button (Stupid German Data Protection Laws)
    driver.find_element(By.CLASS_NAME, "fc-button-label").click()
except:
    pass

try:
    #Checks if the film is foreign and if so, gets its original title
    film_original = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/section[1]/p/em').text
    film_original = film_original.strip("'‘’")
except:
    is_foreign = False

#Get film info
film_year = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/section[1]/p/small/a').text
director = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/section[1]/p/a/span').text

#Get image
my_property = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]"))).value_of_css_property("background-image")
image_link = re.split('[()]',my_property)[1]
image_link = image_link.replace('"','')
urllib.request.urlretrieve(image_link,"C:\\Users\\matte\\Desktop\\pirateboxd\\film.png")
image = Image.open('C:\\Users\\matte\\Desktop\\pirateboxd\\film.png')
image = image.convert("RGBA")