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

print('Please install Chrome and Chrome Web driver befrore running the script. Thanks!')

path = Path(input("Please enter the driver path.\n>").strip())
# Windows -> C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe
# MAC -> X:/Users/username/Desktop

downloads = input("Please enter the path where you would want to store the images.\n>").strip()

keyword = input('Enter the keyword:\n>')

def saveimg(mark,link,fn):
    try:
        page = req.urlopen(link, timeout=10)
        cont = page.read()
        page.close()
    except:
        try:
            response = requests.get(link,timeout = 10)
            if response.status_code == 200:
                cont = response.content
            else:
                raise
        except:
            print(f'Skipped. Not able to access the URL: {link}')
            return 0
    fn = str(mark) + '_' + re.split('[/\\:\|?]',fn)[0].strip()
    if 'jpg' in link:
        f = open(Path(downloads + '\\' + fn + '.jpg'),'wb')
    elif 'png' in link:
        f = open(Path(downloads + '\\' + fn + '.png'),'wb')
    else:
        f = open(Path(downloads + '\\' + fn + '.jpeg'),'wb')
    f.write(cont)
    f.close()
    print('Title: ' + fn + ' ... Downloaded')
    return 1

driver = webdriver.Chrome(path)
driver.get('https://www.google.com/imghp')
search =  WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[1]/div/div[2]/input')))
search.send_keys(keyword)
search.send_keys(Keys.RETURN)

imgReq = int(input('Number of images need to be downloaded:\n>'))

i = 0
inc = 1
limit = 4

while(i<imgReq):
    try:
        thumb = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[' + str(inc) + ']/a[1]')
    except:
        if limit == 0:
            print("\n*Can't find next Element. Limit set to 5 jumps*")
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
    addon = saveimg(i+1, link, alt)
    inc += 1
    i += addon
    limit = 5

driver.quit()