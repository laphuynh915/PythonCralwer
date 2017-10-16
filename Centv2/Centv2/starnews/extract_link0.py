import urllib.request
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import requests

def get_link(url,page_number):
    listUrl = []
    try:
        for x in range(1,page_number+1):
            r  = requests.get("http://kenh14.vn/timeline/laytinmoitronglist-%s"%x + url)

            data = r.text
            soup = BeautifulSoup(data, "lxml")
            for link in soup.find_all('div', class_="knswli-left fl"):
                url1 = link.find('a')
                url2 = url1.get("href")

                img1 = link.find('img')
                img2 = img1.get("src")
                dic = {'img': img2, 'URL': url2}
                listUrl.append(dic)
    except:
        print("Co loi cmnr dit me")

    return listUrl
