import scrapy
from scrapy_splash import SplashRequest
from scrapy.spiders import CrawlSpider
from starnews.items import StarnewsItem
from scrapy.selector import Selector
from starnews import extract_link

class MySpider(CrawlSpider):
    name = 'lifejs'

    def start_requests(self):
        link = extract_link.get_link(1)
        print(link)
        print(len(link))
        for line in link:
            try:
                yield SplashRequest(url="http://kenh14.vn" + line['URL'],callback = self.parse, meta={'url': line['img']})
            except:
                print("Link sai")
        #with open("testfile.txt") as f:
            #for line in f:
                #line = line.replace('\n','')
                #print("%s day la" %line)
                #try:
                    #yield SplashRequest(url=line,callback = self.parse_link,)
                #except:
                    #print("Link sai")

    def parse(self, response):
        pewpew = response.meta.get('url')

        item = StarnewsItem()
        try:
            try:
                item['title'] = Selector(response).css('h1.kbwc-title::text').extract()[0]
            except:
                print("Loi Title")
            try:
                item['content'] = Selector(response).css('div.knc-content').extract()[0]
            except:
                print("Loi Content")
            try:
                item['url'] = response.url
            except:
                print("Loi URL")
            try:
                item['name'] = response.url.split('/')[-1].split('.')[0]
            except:
                print("Loi name")
            try:
                item['thumb'] = pewpew
            except:
                print("Loi thumb")
            yield item
        except:
            print("Loi khi nap thong tin vao item")
