import requests
# import re
from bs4 import BeautifulSoup,element
from requests.exceptions import RequestException
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(soup):
    # html = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?board-item-main.*?<a.*?>(.*?)</a>.*?star">(.*?)</p>'
    #                   + '.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    # results = re.findall(html,text)
    # for result in results:
    #     yield {
    #         'index':result[0],
    #         'title':result[1],
    #         'actor':result[2].strip()[3:],
    #         'time':result[3][5:],
    #         'score':result[4] + result[5]
    #     }
    return {
        'index':soup.i.string,
        'title':soup.select('.name a')[0].get_text(),
        'actor':soup.select('.star')[0].get_text().strip(),
        'time':soup.select('.releasetime')[0].get_text(),
        'score':soup.find(class_='integer').string + soup.find(class_='fraction').string
    }

def write_to_file(text):
    with open('maoyantop100.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(text,ensure_ascii=False) + '\n')

def main(jj):
    url = "https://maoyan.com/board/4?offset=" + str(jj)
    response = get_one_page(url)
    soup = BeautifulSoup(response,'lxml').dl.contents
    # for i in parse_one_page(response):
    #     print(i)
    #     write_to_file(i)
    for su in soup:
        if type(su) == element.Tag:
            write_to_file(parse_one_page(su))

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])