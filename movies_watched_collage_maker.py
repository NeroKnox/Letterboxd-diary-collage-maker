import time
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import re
import urllib.request

if(__name__ == "__main__"):
    #Variables
    username = input("Enter Letterboxd Username: ")
    year = input("Enter Year: ")
    month = input("Enter Month as a number (01-12): ")
    
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
    
    is_film = True
    film_number = 1
    film_names = []
    film_ids = []
    film_links = []
    image_links = []
    
    # Opening Diary
    driver.get('https://letterboxd.com/'+username+'/films/diary/for/'+year+'/'+month+'/')
    time.sleep(5)
    
    #For a Month, get the Names, IDs and Links of all Films in the Month
    while is_film:
        try:
            film_name = driver.find_element(By.XPATH,f'/html/body/div[1]/div/section[2]/table/tbody/tr[{film_number}]/td[3]/div').get_attribute("data-film-name")
            film_names.append(film_name)
            film_link = driver.find_element(By.XPATH,f'/html/body/div[1]/div/section[2]/table/tbody/tr[{film_number}]/td[3]/div').get_attribute("data-film-link")
            film_links.append(film_link)
            film_number += 1
        except:
            is_film = False
            film_number -= 1
            break
    
    #Reverse the arrays, so they are ordered by Earliest Watch First
    film_names.reverse()
    film_links.reverse()

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
    collage = Image.new(mode='RGB',size=((largura*(1200+margin))+margin,(altura*(675+margin))+margin),color=(0,0,0))
    x_coord = margin
    y_coord = margin
    movie_counter = 0
    #Get Images
    driver.implicitly_wait(5)
    for link in film_links:
        driver.get('https://letterboxd.com/'+ link)
        is_foreign = True

        try:
            #Click Consent Button (Stupid German Data Protection Laws)
            driver.find_element(By.CLASS_NAME, "fc-button-label").click()
        except:
            pass

        time.sleep(5)
        driver.switch_to.default_content()

        try:
            #Checks if the film is foreign and if so, gets its original title
            film_original = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/section[1]/p/em').text
            film_original = film_original.strip("'‘’")
        except:
            is_foreign = False
        
        #Get film info
        #film_year = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/section[1]/p/small/a').text
        film_year = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/section[1]/div/div/div/a').text
        #director = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/section[1]/p/a/span').text
        director = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/section[1]/div/div/p/span[2]/a/span').text
        
        
        #Get image
        #my_property = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]"))).value_of_css_property("background-image")
        my_property = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]"))).value_of_css_property("background-image")
        image_link = re.split('[()]',my_property)[1]
        image_link = image_link.replace('"','')
        urllib.request.urlretrieve(image_link,"C:\\Users\\matte\\Desktop\\pirateboxd\\film.png")
        image = Image.open('C:\\Users\\matte\\Desktop\\pirateboxd\\film.png')
        image = image.convert("RGBA")
        
        #Film label
        label = ImageDraw.Draw(collage)
        title_font = ImageFont.truetype('GOTHIC.TTF', 36)
        subtitle_font = ImageFont.truetype('GOTHICI.TTF',24)
        overtitle_font = ImageFont.truetype('GOTHICBI.TTF',30)
        
        #Draw label background
        if is_foreign:
            width = max(title_font.getsize(film_original + ' (' + film_year + ')')[0], subtitle_font.getsize('dir: ' + director)[0], overtitle_font.getsize(film_names[movie_counter])[0])
            plus = 545
        else:
            width = max(title_font.getsize(film_names[movie_counter] + ' (' + film_year + ')')[0], subtitle_font.getsize('dir: ' + director)[0])
            plus = 575
        overlay = Image.new('RGBA', (1200,675), (0,0,0,0))
        rect = ImageDraw.Draw(overlay)
        rect.rectangle([(10,plus),(30+width,665)], fill=(0,0,0,int(255*0.5)))
        image = Image.alpha_composite(image, overlay)
        image = image.convert("RGB")

        #Add image to final collage
        collage.paste(image,(x_coord,y_coord))

        #Add text
        if is_foreign:
            label.text((x_coord+25,y_coord+550),film_names[movie_counter],(255,255,255), font=overtitle_font)
            label.text((x_coord+25,y_coord+580),film_original + ' (' + film_year + ')',(255,255,255), font=title_font)
            label.text((x_coord+25,y_coord+625),'dir: ' + director,(255,255,255), font=subtitle_font)
        else:
            label.text((x_coord+25,y_coord+580),film_names[movie_counter] + ' (' + film_year + ')',(255,255,255), font=title_font)
            label.text((x_coord+25,y_coord+625),'dir: ' + director,(255,255,255), font=subtitle_font)
        
        #Move pointer
        movie_counter +=1
        x_coord += 1200 + margin
        if(movie_counter % largura == 0):
            x_coord = margin
            y_coord += 675 + margin
    
    #Save final collage
    collage.save('C:\\Users\\matte\\Desktop\\pirateboxd\\Movies_'+str(year)+'_'+str(month)+'.jpg')