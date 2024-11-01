import time
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import re
import urllib.request
from guess_language import guess_language

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
    film_ratings = []

    # Opening Diary
    driver.get('https://letterboxd.com/'+username+'/films/diary/for/'+year+'/'+month+'/')
    time.sleep(0.1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);") #scroll to bottom to load all films
    time.sleep(0.1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scroll to bottom to load all films
    time.sleep(0.1)
    
    
    #For a Month, get the Names, IDs and Links of all Films in the Month
    while is_film:
        try:
            film_name = driver.find_element(By.XPATH,f'/html/body/div[1]/div/section[2]/table/tbody/tr[{film_number}]/td[3]/div').get_attribute("data-film-name")
            film_names.append(film_name)
            film_link = driver.find_element(By.XPATH,f'/html/body/div[1]/div/section[2]/table/tbody/tr[{film_number}]/td[3]/div').get_attribute("data-film-link")
            film_links.append(film_link)
            film_rating = driver.find_element(By.XPATH,f'/html/body/div[1]/div/section[2]/table/tbody/tr[{film_number}]/td[5]/div/span').text
            film_ratings.append(film_rating)
            film_number += 1
        except:
            is_film = False
            film_number -= 1
            break
    
    #Reverse the arrays, so they are ordered by Earliest Watch First
    film_names.reverse()
    film_links.reverse()
    film_ratings.reverse()

    #Create Background Image
    margin = 10
    banner = 175
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
    largura_tot = (largura*(1200+margin))+margin
    altura_tot = (altura*(675+margin))+margin+banner
    collage = Image.new(mode='RGB',size=(largura_tot, altura_tot),color=(20,24,28))
    
    #Coordinates Pointers definition
    x_coord = margin
    y_coord = margin+banner
    movie_counter = 0
    
    #Fonts
    title_font = ImageFont.truetype('GOTHIC.TTF', 36)
    subtitle_font = ImageFont.truetype('GOTHICI.TTF',24)
    overtitle_font = ImageFont.truetype('GOTHICBI.TTF',30)
    header_font = ImageFont.truetype('GOTHICB.TTF',80)
    kanji_font = ImageFont.truetype('YuGothR.ttc',36)
    hangul_font = ImageFont.truetype('malgunsl.ttf',36)
    thai_font = ImageFont.truetype('LeelUIsl.ttf',36)
    star_font = ImageFont.truetype('YuGothB.ttc',60)

    #Banner
    draw = ImageDraw.Draw(collage)
    draw.rectangle([(0,0),(largura_tot,banner)], fill=(32,40,48))
    logo = Image.open('C:\\Users\\matte\\Desktop\\pirateboxd\\logo.png')
    logo = logo.resize((250,135))
    collage.paste(logo,(largura_tot - 300,20))
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August','September','October','November','December']
    draw.text((40,42),username+"'s " + months[int(month)-1] + " of '" + year[2:],(255,255,255), font=header_font)

    #Get Images
    driver.implicitly_wait(2)
    for link in film_links:
        driver.get('https://letterboxd.com/'+ link)
        is_foreign = True

        try:
            #Click Consent Button (Stupid German Data Protection Laws)
            driver.find_element(By.CLASS_NAME, "fc-button-label").click()
        except:
            pass

        driver.switch_to.default_content()

        try:
            #Checks if the film is foreign and if so, gets its original title
            film_original = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/section[1]/div/div/h2').text
            film_original = film_original.strip("'‘’")
            language = guess_language(film_original) #original language of movie
        except:
            try:
                film_original = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/section[1]/div/div/h2').text
                film_original = film_original.strip("'‘’")
                language = guess_language(film_original)
            except:
                is_foreign = False
        
        #Get film info
        try:
            film_year = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/section[1]/div/div/div/a').text
            director = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/section[1]/div/div/p/span[2]/a/span').text
            image_source = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]"))).value_of_css_property("background-image")
        except:
            film_year = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/section[1]/div/div/div/a').text
            director = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/section[1]/div/div/p/span[2]/a/span').text
            image_source = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]"))).value_of_css_property("background-image")
        
        #Get image
        image_link = re.split('[()]',image_source)[1]
        image_link = image_link.replace('"','')
        urllib.request.urlretrieve(image_link,"C:\\Users\\matte\\Desktop\\pirateboxd\\film.png")
        image = Image.open('C:\\Users\\matte\\Desktop\\pirateboxd\\film.png')
        image = image.convert("RGBA")
        
        #Draw film label background
        if is_foreign:
            if language in ['ja','zh']:
                width = max(kanji_font.getsize(film_original + ' (' + film_year + ')')[0], subtitle_font.getsize('dir: ' + director)[0], overtitle_font.getsize(film_names[movie_counter])[0])
            elif language == 'ko':
                width = max(hangul_font.getsize(film_original + ' (' + film_year + ')')[0], subtitle_font.getsize('dir: ' + director)[0], overtitle_font.getsize(film_names[movie_counter])[0])
            elif language == 'th':
                width = max(thai_font.getsize(film_original + ' (' + film_year + ')')[0], subtitle_font.getsize('dir: ' + director)[0], overtitle_font.getsize(film_names[movie_counter])[0])
            else:
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
            draw.text((x_coord+25,y_coord+550),film_names[movie_counter],(255,255,255), font=overtitle_font)
            if language in ['ja','zh']:
                draw.text((x_coord+25,y_coord+590),film_original + ' (' + film_year + ')',(255,255,255), font=kanji_font)
            elif language == 'ko':
                draw.text((x_coord+25,y_coord+580),film_original + ' (' + film_year + ')',(255,255,255), font=hangul_font)
            elif language == 'th':
                draw.text((x_coord+25,y_coord+580),film_original + ' (' + film_year + ')',(255,255,255), font=thai_font)
            else:
                draw.text((x_coord+25,y_coord+580),film_original + ' (' + film_year + ')',(255,255,255), font=title_font)
            draw.text((x_coord+25,y_coord+625),'dir: ' + director,(255,255,255), font=subtitle_font)
        else:
            draw.text((x_coord+25,y_coord+580),film_names[movie_counter] + ' (' + film_year + ')',(255,255,255), font=title_font)
            draw.text((x_coord+25,y_coord+625),'dir: ' + director,(255,255,255), font=subtitle_font)
        #Add rating
        #rating_size = star_font.getsize(film_ratings[movie_counter])[0]
        draw.text((x_coord + 1175, y_coord+15), film_ratings[movie_counter], (0,192,48), font=star_font, anchor='rt')

        #Move pointer
        movie_counter +=1
        x_coord += 1200 + margin
        if(movie_counter % largura == 0):
            if(movie_counter == largura * (altura-1)):
                last_row_empty_space = largura - film_number + movie_counter
                x_coord = margin + 600 * (last_row_empty_space)
            else:
                x_coord = margin
            y_coord += 675 + margin
    
    #Save final collage
    collage.save('C:\\Users\\matte\\Desktop\\pirateboxd\\Movies_'+str(username)+'_'+str(year)+'_'+str(month)+'.jpg')
