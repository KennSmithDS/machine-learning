# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OptionChainCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    contract_name = scrapy.Field()
    last_trade = scrapy.Field()
    expiration = scrapy.Field()
    strike = scrapy.Field()
    option_type = scrapy.Field()
    bid = scrapy.Field()
    ask = scrapy.Field()
    change = scrapy.Field()
    perc_change = scrapy.Field()
    volume = scrapy.Field()
    open_interest = scrapy.Field()
    implied_volatility = scrapy.Field()