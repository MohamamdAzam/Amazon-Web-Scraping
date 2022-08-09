from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

data= pd.read_csv("amazon_scraping.csv")


for i in range(1000):
    Asin = data.Asin[i]
    asin = Asin.replace("'", "")
    Country = data.country[i]
    country = Country.replace("'", "")
    URL = f'https://www.amazon.{country}/dp/000{asin}'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    if(soup.find(id='productTitle') == None):
        continue
    
    title = soup.find(id='productTitle').get_text()

    if(soup.find('span', 'a-offscreen') == None):
        price = "Price Unavailable"
    else:
        price = soup.find('span', 'a-offscreen').text

    if(soup.find(id = "imgBlkFront")== None):
        image = "Image Unavailable"
    else:
        image = soup.find(id = "imgBlkFront")['src']

    if (soup.find(id = "detailBullets_feature_div") == None):
        details = "No Details"
    else: 
        details1 = soup.find(id = "detailBullets_feature_div")
        if (details1.ul == None):
            details = "No Details"
        else:
            details2 = details1.ul.text
            details = " ".join(details2.split())
    
    dict = {'Title':title, 'Price':price, 'Image_URL':image, 'Details':details}
    
    def write_json(new_data, filename='products_data.json'):
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data["all_data"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    
    write_json(dict)