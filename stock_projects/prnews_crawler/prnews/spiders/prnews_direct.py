import scrapy
import datetime as dt
import pandas as pd
import re, os
from tqdm import tqdm, trange
import time
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

class GlobeNewsSpiderDirect(scrapy.Spider):
    name = 'prnews_direct'

    def __init__(self, *args,**kwargs):
        super(GlobeNewsSpiderDirect, self).__init__(*args, **kwargs)
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

    def db_url_list(self):
        url_query = """SELECT DISTINCT url FROM articles"""
        url_df = pd.read_sql(url_query, self.conn)
        urls = url_df['url'].unique().tolist()
        return urls

    def start_requests(self):
        try:

            print('Fetching complete article list for date range')
            t1 = time.time()
            urls = self.get_article_list()
            t2 = time.time()
            print(f'Took {t2-t1} seconds to fetch {len(urls)} urls from CSV file')

            print('Querying sqlite database...')
            t1 = time.time()
            crawled_urls = self.db_url_list()
            t2 = time.time()
            print(f'Took {t2-t1} seconds to query {len(crawled_urls)} rows from sqlite database')

            t1 = time.time()
            # urls_left = [url for url in urls if url not in crawled_urls] # <-- I believe this step is taking a long time, >200 billion computations O(n^2)
            urls_left = set(urls) - set(crawled_urls)
            urls_left = list(urls_left)
            t2 = time.time()
            print(f'Took {t2-t1} seconds to remove crawled urls from complete list')

            print(f'Beginning to crawl prnewswire for {len(urls_left)} articles not found in database')
            for this_url in tqdm(urls_left):
                yield scrapy.Request(url=this_url, callback=self.parse_news_article)

        except Exception as e:
            print('-'*80)
            print("Exception in request initiation code block: %s", e)
            traceback.print_exc(file=sys.stdout)
            print('-'*80)

    def ticker_scan(self, par_text):
        try:

            pattern = re.compile(r'NASDAQ\:\s?(\w{2,5})\)|NYSE\:\s?(\w{2,5})\)|OTC.*\:\s?(\w{2,5})\)')
            matches = pattern.findall(par_text)
            ticker_list = []
            if len(matches) > 0:
                [[ticker_list.append(tick.upper()) for tick in tick_tup if len(tick) > 1] for tick_tup in matches]
            return list(set(ticker_list))

        except Exception as e:
            print('-'*80)
            print("Exception in ticker scan code block: %s", e)
            traceback.print_exc(file=sys.stdout)
            print('-'*80)

    def parse_news_article(self, response):
        try:

            url = response.url
            body_text = response.xpath('//div[@class="col-sm-10 col-sm-offset-1"]//p//text()').extract()
            # body_text = response.xpath('//section[@class="release-body container"]//div//div//p//text()').extract()
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
            print('-'*80)
            print("Exception in article parsing code block: %s", e)
            traceback.print_exc(file=sys.stdout)
            print('-'*80)

    @ staticmethod
    def get_article_list():
        try:

            recent_url_df = pd.read_csv('C://Users//kenns//Documents//StockProject//prnews//prnews//recent_sitemap_urls.csv')
            recent_url_df.dropna(inplace=True)
            # recent_url_df2 = recent_url_df[~recent_url_df['dt'].isin(['2019-12', '2019-11'])].copy()
            recent_url_df['dt_dt'] = recent_url_df['dt'].apply(lambda x: dt.datetime.strptime(x, "%Y-%m"))
            # recent_url_df2 = recent_url_df[(recent_url_df['dt_dt']<dt.datetime.strptime("2020-05", "%Y-%m")) & (recent_url_df['dt_dt']>dt.datetime.strptime("2019-10", "%Y-%m"))].copy()
            recent_url_df2 = recent_url_df[recent_url_df['dt_dt']<dt.datetime.strptime("2018-02", "%Y-%m")].copy()
            recent_url_df2.sort_values(by='dt_dt', ascending=False, inplace=True)
            min_dt = recent_url_df2['dt_dt'].min()
            max_dt = recent_url_df2['dt_dt'].max()
            print(f'Planning to crawl {len(recent_url_df2)} articles in archive CSV file between dates {min_dt} and {max_dt}')
            return recent_url_df2.url.unique().tolist()

        except Exception as e:
            print('-'*80)
            print("Exception in article archive retrieval code block: %s", e)
            traceback.print_exc(file=sys.stdout)
            print('-'*80)