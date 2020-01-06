# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class anjukeHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #城市名
    city = scrapy.Field()

    #楼盘名称
    name = scrapy.Field()

    #位置
    address = scrapy.Field()

    # 类型
    type = scrapy.Field()

    # 户型
    huxing = scrapy.Field()

    # 楼层数
    louceng = scrapy.Field()

    #户数
    hushu = scrapy.Field()

    #交房时间
    submitTime = scrapy.Field()

    # #栋数
    # ridgepole = scrapy.Field()
    #均价
    price = scrapy.Field()

    #区域
    field = scrapy.Field()
    pass


class lianjiaHouseItem(scrapy.Item):

    city = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    ridgepole = scrapy.Field()
    hushu = scrapy.Field()
    address = scrapy.Field()
    type = scrapy.Field()
    pass
