import scrapy
import datetime as dt
import re, os
import sys, traceback
# import logging
# from scrapy.utils.log import configure_logging  

current_dt = dt.datetime.now()
current_dt_str = current_dt.strftime('%Y_%m_%d_%H_%M_%S')

# configure_logging(install_root_handler = False) 
# logging.basicConfig (filename = f'logging_{current_dt_str}.log', format = '%(levelname)s: %(your_message)s', level = logging.INFO)

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

    def start_requests(self):
        urls = ['https://www.prnewswire.com/news-releases/news-releases-list/?page=1&pagesize=100']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def ticker_scan(self, par_text):
        try:

            pattern = re.compile(r'NASDAQ\:\s?(\w{2,5})\)|NYSE\:\s?(\w{2,5})\)|OTC.*\:\s?(\w{2,5})\)')
            matches = pattern.findall(par_text)
            if len(matches) > 0:
                ticker_list = [tick.upper() for tick in matches[0] if len(tick) > 1]
            else:
                ticker_list = []
            return ticker_list

        except Exception as e:
            self.logger.error('-'*80)
            self.logger.error("Exception in ticker scan code block: %s", e)
            # self.logger.error(traceback.print_exc(file=sys.stdout))
            self.logger.error('-'*80)

    def parse(self, response):
        try:

            for article in response.xpath('//div[@class="col-sm-8 col-lg-9 pull-left card"]//h3//a//@href').extract():
            # for article_row in response.xpath('//div[@class="col-sm-8 col-lg-9 pull-left card"]//h3').extract():
                if article is not None:
                    article_url = base_url + article
                    self.logger.info('Parsing article: %s', article_url)
                    article_crawl = response.urljoin(article_url)
                    yield scrapy.Request(article_crawl, callback=self.parse_news_article, headers=headers)
            self.logger.info('Finished parsing articles on page: %s', response.url)

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

    def parse_news_article(self, response):
        try:

            body_text = response.xpath('//div[@class="col-sm-10 col-sm-offset-1"]//p//text()').extract()
            paragraphs = ''.join(body_text).upper()
            # paragraphs = paragraphs.replace(' )', ')')
            ticker_list = self.ticker_scan(paragraphs)
            yield {
                "title": response.xpath('//div[@class="col-sm-7 col-sm-offset-1 col-vcenter col-xs-12 "]//h1/text()').extract_first(),
                "date_published": response.xpath('//p[@class="mb-no"]//text()').extract_first(),
                "body_text": body_text,
                "tickers": ticker_list
            }

        except Exception as e:
            self.logger.error('-'*80)
            self.logger.error("Exception in article parsing code block: %s", e)
            # self.logger.error(traceback.print_exc(file=sys.stdout))
            self.logger.error('-'*80)