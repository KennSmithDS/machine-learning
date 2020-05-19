import scrapy
import datetime as dt
import pandas as pd
import re, os
import sqlite3
from datetime import datetime, timedelta
import sys, traceback

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
    name = 'prnews'

    def __init__(self, pr_year=0, pr_month=0, pr_day=0, article_dt=None, *args,**kwargs):
        super(GlobeNewsSpider, self).__init__(*args, **kwargs)
        self.pr_year = pr_year
        self.pr_month = pr_month
        self.pr_day = pr_day
        self.last_article_dt = article_dt
        self.db_connection()

    def db_connection(self):
        self.conn = sqlite3.connect('C://Users//kenns//Documents//StockProject//prnews//prnews//prnews_articles.db')
        self.curr = self.conn.cursor()

    def item_db_check(self, url_to_check):
        self.curr.execute("""SELECT url FROM articles WHERE url = ?""", (url_to_check, ))
        rows = self.curr.fetchall()
        if len(rows) == 0:
            return False
        else:
            return True

    def start_requests(self):
        # if self.pr_year is not None and self.pr_month is not None and self.pr_day is not None:
        #     urls = [f'https://www.prnewswire.com/news-releases/news-releases-list/?month={self.pr_month}&day={self.pr_day}&year={self.pr_year}&hour=00&page=1&pagesize=100']
        # else:
        #     urls = ['https://www.prnewswire.com/news-releases/news-releases-list/?page=1&pagesize=100']
        urls = self.get_url_date_list()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def ticker_scan(self, par_text):
        try:

            pattern = re.compile(r'NASDAQ\:\s?(\w{2,5})\)|NYSE\:\s?(\w{2,5})\)|OTC.*\:\s?(\w{2,5})\)')
            matches = pattern.findall(par_text)
            ticker_list = []
            if len(matches) > 0:
                [[ticker_list.append(tick.upper()) for tick in tick_tup if len(tick) > 1] for tick_tup in matches]
            return list(set(ticker_list))

        except Exception as e:
            self.logger.error('-'*80)
            self.logger.error("Exception in ticker scan code block: %s", e)
            traceback.print_exc(file=sys.stdout)
            self.logger.error('-'*80)

    def parse(self, response):
        try:
            print('-'*80)
            self.logger.info('-'*80)
            print(f'Parsing articles on page: {response.url}')
            self.logger.info('Parsing articles on page: %s', response.url)

            for article in response.xpath('//div[@class="col-sm-8 col-lg-9 pull-left card"]//h3//a//@href').extract():
                if article is not None:
                    article_url = base_url + article
                    if not self.item_db_check(article_url):
                        article_crawl = response.urljoin(article_url)
                        yield scrapy.Request(article_crawl, callback=self.parse_news_article, headers=headers)
                    else:
                        print(f'Row with url {article_url} found in database')
            self.logger.info('Finished parsing articles on page: %s', response.url)
            print(f'Finished parsing articles on page: {response.url}')

            next_path = response.xpath('//a[@aria-label="Next"]//@href').extract_first()
            if next_path is not None:
                article_dates = response.xpath('//div[@class="col-sm-8 col-lg-9 pull-left card"]//h3//small//text()').extract()
                last_article_date = article_dates[-1]
                self.last_article_dt = dt.datetime.strptime(last_article_date[:-3], "%b %d, %Y, %H:%M")
                self.logger.info('Scrolling to page: %s', next_path)
                next_page = base_url + next_path
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse, headers=headers)
            else:
                self.logger.info('No more links for page: %s', response.url)
                next_page = base_url + f'/news-releases/news-releases-list/?month={self.last_article_dt.month}&day={self.last_article_dt.day}&year={self.last_article_dt.year}&hour={self.last_article_dt.hour}&page=1&pagesize=100'
                self.logger.info('Setting next page to last seen article timestamp: %s', next_page)
                yield scrapy.Request(next_page, callback=self.parse, headers=headers)

        except Exception as e:
            self.logger.error('-'*80)
            self.logger.error("Exception in news list parsing code block: %s", e)
            traceback.print_exc(file=sys.stdout)
            self.logger.error('-'*80)

    def parse_news_article(self, response):
        try:

            url = response.url
            self.logger.info('Parsing article: %s', url)
            body_text = response.xpath('//div[@class="col-sm-10 col-sm-offset-1"]//p//text()').extract()
            paragraphs = ''.join(body_text)
            upper_paragraphs = paragraphs.upper()
            ticker_list = self.ticker_scan(upper_paragraphs)
            ticker_string = ', '.join(ticker_list)
            yield {
                "url": url,
                "title": response.xpath('//header[@class="container release-header"]//div//div//h1//text()').extract_first(),
                "date_published": response.xpath('//p[@class="mb-no"]//text()').extract_first(),
                "body_text": paragraphs,
                "tickers": ticker_string
            }

        except Exception as e:
            self.logger.error('-'*80)
            self.logger.error("Exception in article parsing code block: %s", e)
            traceback.print_exc(file=sys.stdout)
            self.logger.error('-'*80)

    @ staticmethod
    def get_url_date_list():
        url_date_list = []
        date_list = pd.date_range(start="2020-03-11", end="2020-03-11").tolist()
        for this_date in reversed(date_list):
            this_month = this_date.month
            this_day = this_date.day
            this_year = this_date.year
            this_hour = this_date.hour
            this_url = f'https://www.prnewswire.com/news-releases/news-releases-list/?month={this_month}&day={this_day}&year={this_year}&hour={this_hour}&page=1&pagesize=100'
            url_date_list.append(this_url)
        return url_date_list