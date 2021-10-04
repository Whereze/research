from bs4 import BeautifulSoup
from bs4.builder import HTMLTreeBuilder
import requests
import wikipedia
import csv
import re
wikipedia.set_lang("ru")

def get_all_waterfalls_from_csv():
    all_waterfalls = []
    with open("waterfalls_database.csv","r",encoding="utf-8") as f:
        fields = ['title', 'summary', 'url']
        reader = csv.DictReader(f, fields, delimiter=';')
        header = next(reader)
        if header != None:
            for row in reader:
                all_waterfalls.append(
                    {
                    'title':row['title'],
                    'summary':row['summary'],
                    'url':row['url']
                })
    return all_waterfalls     

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException,ValueError):
        print("Сетевая ошибка")
        return False
        
all_waterfalls = get_all_waterfalls_from_csv()

def get_waterfalls_details():
    for waterfall in all_waterfalls:
        waterfall_html = get_html(waterfall['url'])
        try:
            soup = BeautifulSoup(waterfall_html,features="html.parser")
            waterfall_details = soup.find("table", {"data-name" : "Водопад"})
            if waterfall_details:
                height= waterfall_details.find("th",string= re.compile("Высота"))
                if height:
                    height = height.next_sibling.text
                    if height:
                        waterfall['height'] = height          
                width= waterfall_details.find("th",string= re.compile("Ширина"))
                if width:
                    width = width.next_sibling.text
                    if width:
                        waterfall['width'] = width          
                river= waterfall_details.find("th",string= re.compile("Рек"))
                if river:
                    river = river.next_sibling.text 
                    if river:
                        waterfall['river'] = river                                 
                country= waterfall_details.find("th",string= re.compile("Стран"))
                if country:
                    country = country.next_sibling.text     
                    if country:
                        waterfall['country'] = country     
                region= waterfall_details.find("th",string= re.compile("Регион"))      
                if region:
                    region = region.next_sibling.text  
                    if region:
                        waterfall['region'] = region  
                RF_subject= waterfall_details.find("th",string= re.compile("Субъект РФ"))        
                if RF_subject:
                    RF_subject = RF_subject.next_sibling.text  
                    if RF_subject:
                        waterfall['RF_subject'] = RF_subject                              

        except(TypeError,ValueError):
            continue                
    return all_waterfalls


# print(get_waterfalls_details())