from bs4 import BeautifulSoup
from bs4.builder import HTMLTreeBuilder
import requests
import wikipedia
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
        return  result     
    return False     

            
waterfalls_result = get_waterfalls()
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
                

if __name__ == "__main__":
    result = get_waterfalls_pages()
    print(result)
