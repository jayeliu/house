# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class bublelistItem(scrapy.Item):
    unId = scrapy.Field()
    name = scrapy.Field()
    cityId = scrapy.Field()
    groupType = scrapy.Field()
    count = scrapy.Field()
    countUnit = scrapy.Field()
    price = scrapy.Field()
    priceUnit = scrapy.Field()
    border = scrapy.Field()
    lng = scrapy.Field()
    lat  = scrapy.Field()

class houslistItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    cityId = scrapy.Field()
    resblockId = scrapy.Field()
    coverPic = scrapy.Field()
    priceStr = scrapy.Field()
    unitPriceStr = scrapy.Field()
    cardType = scrapy.Field()
    actionUrl = scrapy.Field()
    layout = scrapy.Field()
    areaStr = scrapy.Field()
    orientation = scrapy.Field()
    community = scrapy.Field()
    price = scrapy.Field()
    unitPrice = scrapy.Field()
    area = scrapy.Field()
