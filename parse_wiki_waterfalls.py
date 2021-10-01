from bs4 import BeautifulSoup
from bs4.builder import HTMLTreeBuilder
import requests
import wikipedia
import csv
import re
wikipedia.set_lang("ru")


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException,ValueError):
        print("Сетевая ошибка")
        return False

def get_waterfalls():
    html = get_html("https://ru.wikipedia.org/wiki/Категория:Водопады_по_алфавиту")
    if html:
        soup = BeautifulSoup(html,features="html.parser")
        all_waterfalls = soup.findAll("li")
        result = []    
        for waterfall in all_waterfalls:
            title =  waterfall.find('a')
            # url = waterfall.find('a')
            if title:
                    title = title.text
                    # url = url['href']
                    result.append({
                        "title":title,
                        # "url":url,
                    })
        return result
    return False     

def get_waterfalls_second_page():
    html = get_html("https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%92%D0%BE%D0%B4%D0%BE%D0%BF%D0%B0%D0%B4%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=%D0%A0%D1%8C%D1%8E%D0%BA%D0%B0%D0%BD%D1%84%D0%BE%D1%81%D1%81%D0%B5%D0%BD%0A%D0%A0%D1%8C%D1%8E%D0%BA%D0%B0%D0%BD%D1%84%D0%BE%D1%81%D1%81%D0%B5%D0%BD#mw-pages")
    if html:
        soup = BeautifulSoup(html,features="html.parser")
        all_waterfalls = soup.findAll("li")
        result = []    
        for waterfall in all_waterfalls:
            title =  waterfall.find('a')
            # url = waterfall.find('a')
            if title:
                    title = title.text
                    # url = url['href']
                    result.append({
                        "title":title,
                        # "url":url,
                    })
        return result
    return False  


result_first_page = get_waterfalls()
result_second_page = get_waterfalls_second_page()
waterfalls_result = result_first_page + result_second_page


def get_waterfalls_pages():
    waterfalls_list = []
    for water in waterfalls_result:
        try:
            try:
                water = str(water['title'])
                if water != '':
                    if wikipedia.summary(water):
                        waterfalls_list.append({
                            'title':water,
                            'summary':wikipedia.summary(water)
                        })
            except(TypeError,ValueError):
                continue
        except (wikipedia.exceptions.DisambiguationError,wikipedia.exceptions.PageError):
            continue
    return waterfalls_list

# if __name__ == "__main__":
#     print(get_waterfalls_pages())
