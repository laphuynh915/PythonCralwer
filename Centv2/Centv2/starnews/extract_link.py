from urllib2 import urlopen
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import requests

def get_link(urls,page_number):
    listUrl = []
    try:
        for url in urls:
            for x in range(1,page_number+1):
                r  = urlopen("http://kenh14.vn/timeline/laytinmoitronglist-%s"%(page_number + 1 - x) + url)


                soup = BeautifulSoup(r, "lxml")
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
