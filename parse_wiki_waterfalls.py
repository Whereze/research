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

def get_waterfalls(html):
    if html:
        soup = BeautifulSoup(html,features="html.parser")
        all_waterfalls = soup.find(class_="mw-category-generated")
        result = []
        if all_waterfalls:
            all_waterfalls = all_waterfalls.findAll("li")    
            for waterfall in all_waterfalls:
                title =  waterfall.find('a')
                url = waterfall.find('a')
                if title:
                    if url:
                            title = title.text
                            url = url['href']
                            result.append({
                                "title":title,
                                "url":url,
                            })
        return result
    return False     

html = get_html("https://ru.wikipedia.org/wiki/Категория:Водопады_по_алфавиту")
result_first_page = get_waterfalls(html)

def get_second_page_url(html_main):
    if html_main:
        soup = BeautifulSoup(html,features="html.parser")
        all_waterfalls = soup.find("a",string= "Следующая страница")
        all_waterfalls = "https://ru.wikipedia.org"+all_waterfalls['href']
        return all_waterfalls

html_second_page = get_second_page_url(html)
html_second_page = get_html(html_second_page)
result_second_page = get_waterfalls(html_second_page)



waterfalls_result = result_first_page + result_second_page

def get_waterfalls_pages():
    waterfalls_list = []
    for waterfall in waterfalls_result:
        try:
            try:
                title = str(waterfall['title'])
                url = waterfall['url']
                if title != '':
                    if wikipedia.summary(title):
                        waterfalls_list.append({
                            'title':title,
                            'summary':wikipedia.summary(title),
                            'url':'https://ru.wikipedia.org'+url
                        })
            except(TypeError,ValueError):
                continue
        except (wikipedia.exceptions.DisambiguationError,wikipedia.exceptions.PageError):
            continue
    return waterfalls_list

# if __name__ == "__main__":
#     print(get_waterfalls_pages())
