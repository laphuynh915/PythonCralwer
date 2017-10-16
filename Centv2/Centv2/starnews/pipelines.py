# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
from starnews import post_worldpress

class StarnewsPipeline(object):
    def process_item(self, item, spider):
        try:
            date = time.strftime('%Y-%m-%d %H:%M:%S')
            post_worldpress.insert_post(item['title'],"",item['content'],item['name'],item['url'],date,item['thumb'],item['category'],item['tags'])
            print("***********************************************")
        except:
            print("Huehue")
        return item
