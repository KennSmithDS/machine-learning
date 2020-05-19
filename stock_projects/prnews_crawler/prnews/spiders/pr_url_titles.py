import scrapy
import datetime as dt
from datetime import datetime, timedelta
import re, os
import sys, traceback
import pandas as pd
import json

current_dt = dt.datetime.now()
current_dt_str = current_dt.strftime('%Y_%m_%d_%H_%M_%S')

base_url = 'https://www.prnewswire.com'

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

class GlobeNewsSpider(scrapy.Spider):
    name = 'pr_url_titles'

    def start_requests(self):
        urls = self.get_url_date_list()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        try:

            titles = response.xpath('//div[@class="col-sm-8 col-lg-9 pull-left card"]//h3//a[@class="news-release"]//text()').extract()
            urls = response.xpath('//div[@class="col-sm-8 col-lg-9 pull-left card"]//h3//a[@class="news-release"]//@href').extract()
            crawled = ['False'] * len(titles)

            for i in range(len(titles)):
                yield {
                    "url": urls[i],
                    "title": titles[i],
                    "crawl": crawled[i]
                }

            next_path = response.xpath('//a[@aria-label="Next"]//@href').extract_first()
            if next_path is not None:
                self.logger.info('Scrolling to page: %s', next_path)
                next_page = base_url + next_path
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse, headers=headers)

            self.logger.info('No more links for next page: %s', response.url)

        except Exception as e:
            self.logger.error('-'*80)
            self.logger.error("Exception in news list parsing code block: %s", e)
            # self.logger.error(traceback.print_exc(file=sys.stdout))
            self.logger.error('-'*80)

    @ staticmethod
    def get_url_date_list():
        url_date_list = []
        # date_list = pd.date_range(start="2020-01-01", end="2020-04-29").tolist()
        date_list = pd.date_range(start="2016-01-01", end=dt.datetime.now()).tolist()
        for this_date in reversed(date_list):
            prev_date = this_date - timedelta(days=1)
            this_month = prev_date.month
            this_day = prev_date.day
            this_year = prev_date.year
            this_url = f'https://www.prnewswire.com/news-releases/news-releases-list/?month={this_month}&day={this_day}&year={this_year}&hour=00&page=1&pagesize=100'
            url_date_list.append(this_url)
        return url_date_list