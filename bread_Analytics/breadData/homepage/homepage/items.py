# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
    
class HomepageItem(scrapy.Item):
    # shop_id = scrapy.Field()
    url = scrapy.Field()
    head = scrapy.Field()
    body = scrapy.Field()
