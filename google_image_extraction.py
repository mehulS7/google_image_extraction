from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib import request as req
import re
from pathlib import Path
import time
import requests

print('Please install Chrome and Chrome Web driver befrore running the script. Thanks')

path = Path(input("Please enter the driver path.\n>").strip())
# Windows -> C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe
# MAC -> X:/Users/username/Desktop

downloads = input("Please enter the path where you would want to store the images.\n>").strip()

keyword = input('Enter the keyword:\n>')

def saveimg(mark,link,fn):
    try:
        response = requests.get(link)
        cont = response.content
    except:
        page = req.urlopen(link)
        cont = page.read()
        page.close()
    fn = str(mark) + '_' + re.split('[/\\:\|?]',fn)[0].strip()
    print('Title: ' + fn + ' ... Downloaded')
    f = open(Path(downloads + '\\' + fn + '.png'),'wb')
    f.write(cont)
    f.close()
    

# def movetab(mark,alt):
#     time.sleep(1)
#     driver.switch_to.window(driver.window_handles[1])
#     time.sleep(4)
#     page2_soup = soup(driver.page_source,'html.parser')
#     link = page2_soup.find('img',{'alt' : alt})['src']
#     saveimg(mark,link,alt)
#     driver.close()

driver = webdriver.Chrome(path)
driver.get('https://www.google.com/imghp')
search =  WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[1]/div/div[2]/input')))
search.send_keys(keyword)
search.send_keys(Keys.RETURN)
# time.sleep(2)
# page_soup = soup(driver.page_source,'html.parser')
# imgs = page_soup.findAll('img',{'class' : 'rg_i Q4LuWd'})

# print(f'Maximum number of images that can be downloaded are: {len(imgs)}')

# if len(imgs) !=0:
    
imgReq = int(input('Number of images need to be downloaded:\n>'))

i = 0
inc = 1
limit = 4

while(i<imgReq):
    try:
        thumb = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[' + str(inc) + ']/a[1]')
    except:
        if limit == 0:
            print("Can't find next Element. Limit set to 5 jumps.")
            break
        limit -= 1
        inc += 1
        continue
    print('Image: ',i+1)
    thumb.click()
    time.sleep(5)
    bigImg = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img')))
    alt = bigImg.get_attribute('alt')
    link = bigImg.get_attribute('src')
    print('alt:',alt,'\nlink: ',link)
    saveimg(i+1, link, alt)
    # thumb.send_keys(Keys.CONTROL + Keys.RETURN)
    # movetab(i+1,alt)
    # driver.switch_to.window(driver.window_handles[0])
    inc += 1
    i += 1
    limit = 5

driver.quit()