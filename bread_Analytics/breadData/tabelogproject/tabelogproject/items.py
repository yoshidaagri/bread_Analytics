# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TabelogprojectItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    name = scrapy.Field()
    score = scrapy.Field()
    link = scrapy.Field()
    item = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    homepage = scrapy.Field()
    adress = scrapy.Field()