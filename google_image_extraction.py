from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as soup
from urllib import request as req
import re

print('Please install Chrome and Chrome driver befrore running the script. Thanks')

path = input("Please enter the driver path.\nExample: C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe\n>").strip()
#C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe

downloads = input("Please enter the path where you would want to store the images.\nExample: C:\\Users\\yourname\\Images\n>").strip()
#'C:\Users\yourname\images'

keyword = input('Enter the keyword:\n>')

def saveimg(mark,link,fn):
    page = req.urlopen(link)
    cont = page.read()
    page.close()
    fn = str(mark) + '_' + re.split('[/\\:\|?]',fn)[0].strip()
    print('Title: ' + fn + ' ... Downloaded')
    f = open(downloads + '\\' + fn + '.png','wb')
    f.write(cont)
    f.close()
    

driver = webdriver.Chrome(path)
driver.get('http://google.com/images')
driver.minimize_window()
search =  WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[1]/div/div[2]/input')))
search.send_keys(keyword)
search.send_keys(Keys.RETURN)
driver.implicitly_wait(5)
page_soup = soup(driver.page_source,'html.parser')
imgs = page_soup.findAll('img',{'class' : 'rg_i Q4LuWd'})
print(f'Maximum number of images that can be downloaded are: {len(imgs)}')

if len(imgs) !=0:
    imgReq = int(input('Number of images need to be downloaded:\n>'))

for n,im in enumerate(imgs):
    if n+1 > imgReq:
        break
    else:
        print('Image no: ',n+1)
        if 'src' in im.attrs.keys():
            saveimg(n+1,im['src'],im['alt'])
        else:
            saveimg(n+1,im['data-src'],im['alt'])

driver.quit()
