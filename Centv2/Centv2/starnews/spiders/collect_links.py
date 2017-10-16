from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

class StackSpider(scrapy.Spider):
    name = "collect_link"
    start_urls = [
        "http://kenh14.vn/timeline/laytinmoitronglist-1-2-1-1-1-1-1-0-3-1.chn",
    ]
    data = []

    def parse(self, response):
        for x in range(1,10):
            url = 'http://kenh14.vn/timeline/laytinmoitronglist-' + str(x) + '-2-1-1-1-1-1-0-3-1.chn'
            print("Link hien tai: %s" %url)
            try:
                 yield scrapy.Request(url, callback=self.parse_link)
            except:
                print("Khong the parse link nay")

    def parse_link(self, response):
        file = open("testfile.txt","a")
        self.data = response.css('h3.knswli-title a::attr(href)').extract()
        s = ''.join(self.data)

        for x in self.data:
            s = "http://kenh14.vn" + ''.join(x) + '\n'
            file.write(s)
        file.close()
