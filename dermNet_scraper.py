import json
import os

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

home_url = "https://dermnetnz.org"
base_url = "https://dermnetnz.org/image-library/imagesJson"

# initialize chrome driver
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

folder_name = 'thumbnail_images'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

# get json response from api
def get_json_from_dermnet_api():
    driver.get(base_url)
    text_resp = driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML')
    json_resp = json.loads(text_resp)
    driver.close()
    return json_resp

# function to download images
def download_images(json_resp):

    # change to created directory
    os.chdir(os.path.join(os.getcwd(), folder_name))

    for j in json_resp:
        thumbnail_name = ''
        thumbnail_name = j['thumbnail'].rsplit('/', 1)[-1]
        if not thumbnail_name:
            thumbnail_name = j['name'] + '.jpg'
        
        # saving image using request library
        with open(thumbnail_name, 'wb') as f:
            try:
                r = requests.get(j['thumbnail'])
            except Exception as e:
                print("Exception-{}-while-downloading-thumbnail-{}".format(e, j['thumbnail']))
                continue
            f.write(r.content)

        # code to save image just using selenium 
        # driver.implicitly_wait(5)
        # driver.get(j['thumbnail'])
        # driver.save_screenshot(thumbnail_name)
    print("Images Downloaded !")
    return 

# save json respose in required format to csv
def save_json_to_csv(json_resp):
    for j in json_resp:

        if 'url' in j and j['url']:
            url = home_url + j['url']
            j['url'] = url

        if 'name' in j and j['name']:
            filtered_name = j['name'].removesuffix('images')
            j['name'] = filtered_name.strip(' ')

        if 'page_name' in j and j['page_name']:
            del j['page_name'] 
    df = pd.json_normalize(json_resp)
    df.to_csv('dermNet_scraped_data.csv', encoding='utf-8-sig', index=False, columns=['name', 'thumbnail', 'url'])
    
    print("Csv File created !")
    return 

def scrape_dermnet():
    json_resp = get_json_from_dermnet_api()
    
    save_json_to_csv(json_resp)

    download_images(json_resp)

    return

if __name__ == "__main__":
    scrape_dermnet()
    print("Scraping of dermnet completed!")
    driver.quit()