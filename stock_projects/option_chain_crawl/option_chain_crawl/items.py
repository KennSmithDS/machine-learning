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
    strike = scrapy.Field()
    last = scrapy.Field()
    bid = scrapy.Field()
    ask = scrapy.Field()
    change = scrapy.Field()
    perc_change = scrapy.Field()
    volume = scrapy.Field()
    open_interest = scrapy.Field()
    implied_volatility = scrapy.Field()
    expiration = scrapy.Field()
    option_type = scrapy.Field()

    # item['contract_name'] = row.xpath('.//td[1]//text()').get()
    # item['last_trade'] = row.xpath('.//td[2]//text()').get()
    # item['strike'] = row.xpath('.//td[3]//text()').get()
    # item['last'] = row.xpath('.//td[4]//text()').get()
    # item['bid'] = row.xpath('.//td[5]//text()').get()
    # item['ask'] = row.xpath('.//td[6]//text()').get()
    # item['change'] = row.xpath('.//td[7]//text()').get()
    # item['perc_change'] = row.xpath('.//td[8]//text()').get()
    # item['volume'] = row.xpath('.//td[9]//text()').get()
    # item['open_interest'] = row.xpath('.//td[10]//text()').get()
    # item['implied_volatility'] = row.xpath('.//td[11]//text()').get()
    # item['expiration'] = response.meta['expiry']
    # item['option_type'] = 'put'