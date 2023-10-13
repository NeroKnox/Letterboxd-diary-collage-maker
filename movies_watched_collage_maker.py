import time
import math
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import re
import urllib.request

if(__name__ == "__main__"):
    service = Service(r"C:\\Program Files\\Google\\Chrome\\Application\\chromedriver-win64\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options) 
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'MyApp/1.0')]
    urllib.request.install_opener(opener)
    
    #Variables
    '''
    username = input("Enter Letterboxd Username: ")
    year = input("Enter Year: ")
    month = input("Enter Month as a number (01-12): ")
    '''

    username = 'neroknox'
    year = '2023'
    month = '09'
    x = 0
    film_number = 1
    film_names = []
    film_ids = []
    film_links = []
    image_links = []
    
    # Opening Diary
    driver.get('https://letterboxd.com/'+username+'/films/diary/for/'+year+'/'+month+'/')
    time.sleep(1)
    
    #For a Month, get the Names, IDs and Links of all Films in the Month
    while x == 0:
        try:
            film_name = driver.find_element(By.XPATH,f'/html/body/div[1]/div/section[2]/table/tbody/tr[{film_number}]/td[3]/div').get_attribute("data-film-name")
            film_names.append(film_name)
            film_id = driver.find_element(By.XPATH,f'/html/body/div[1]/div/section[2]/table/tbody/tr[{film_number}]/td[3]/div').get_attribute("data-film-id")
            film_ids.append(film_id)
            film_link = driver.find_element(By.XPATH,f'/html/body/div[1]/div/section[2]/table/tbody/tr[{film_number}]/td[3]/div').get_attribute("data-film-link")
            film_links.append(film_link)
            film_number += 1
        except:
            x = 1
            film_number -= 1
            break
    
    #Create Background Image
    margin = 10
    if film_number <= 3:
        largura = 1
        altura = film_number
    else:
        largura = 2
        altura = 2
        while film_number > (largura*altura):
            if altura == largura:
                altura += 1
            else:
                largura += 1
    #individual image size - height: 675 px width: 1200 px
    #Original color: 12,44,68 (dark blue)
    collage = Image.new(mode='RGB',size=((largura*(1200+margin))+margin,(altura*(675+margin))+margin),color=(0,0,0))
    x_coord = margin
    y_coord = margin
    row_counter = 0
    #Get Images
    for link in film_links:
        driver.get('https://letterboxd.com/'+ link)
        try:
            #Click Consent Button (Stupid German Data Protection Laws)
            driver.find_element(By.CLASS_NAME, "fc-button-label").click()
        except:
            pass
        my_property = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]"))).value_of_css_property("background-image")
        print(my_property)
        image_link = re.split('[()]',my_property)[1]
        image_link = image_link.replace('"','')
        print(image_link)
        #image_link=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div[2]"))).get_attribute('srcset')
        #response = requests.get(image_link)
        #img = Image.open(BytesIO(response.content))
        #urlretrieve(image_link,'film.png')
        urllib.request.urlretrieve(image_link,"C:\\Users\\matte\\Desktop\\pirateboxd\\film.png")
        image = Image.open('C:\\Users\\matte\\Desktop\\pirateboxd\\film.png')
        #Add image to final collage
        collage.paste(image,(x_coord,y_coord))
        #Move pointer
        row_counter +=1
        x_coord += 1200 + margin
        if(row_counter == largura):
            x_coord = margin
            y_coord += 675 + margin
            row_counter = 0
    
    #Save final collage
    collage.save('C:\\Users\\matte\\Desktop\\pirateboxd\\Movies_'+str(year)+'_'+str(month)+'.jpg')