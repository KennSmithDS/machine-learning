import scrapy
import datetime as dt
import re, os

current_dt = dt.datetime.now()
current_dt_str = current_dt.strftime('%Y_%m_%d_%H_%M_%S')
base_url = 'https://www.globenewswire.com/'

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
    name = 'globenews'

    def start_requests(self):
        urls = ['https://www.globenewswire.com/Index?page=1#pagerPos']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def ticker_scan(self, par_text):
        pattern = re.compile(r'Nasdaq.*\:(\w{2,5})\)|Nasdaq.*\:.(\w{2,5})\)|NASDAQ.*\:.(\w{2,5})\)|NASDAQ.*\:(\w{2,5})\)|NYSE.*\:.(\w{2,5})\)|NYSE.*\:(\w{2,5})\)|OTC.*\:.(\w{2,5})\)|OTC.*\:(\w{2,5})\)')
        matches = pattern.findall(par_text)
        if len(matches) > 0:
            ticker_list = [tick for tick in matches[0] if len(tick) > 1]
        else:
            ticker_list = []
        return ticker_list

    def parse(self, response):
        
        for article in response.xpath('//*[@class="rl-container"]//a//@href').extract():
            article_url = base_url + article
            if article_url is not None:
                article_crawl = response.urljoin(article_url)
                yield scrapy.Request(article_crawl, callback=self.parse_news_article, headers=headers)

        next_path = response.xpath('//li[@class="ui-html-pager-next"]//a//@href').extract_first()
        next_page = base_url + next_path
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, headers=headers)

    def parse_news_article(self, response):
        body_text = response.xpath('//span[@class="article-body"]//p//text()').extract()
        first_paragraphs = ', '.join(body_text[0:4])
        ticker_list = self.ticker_scan(first_paragraphs)
        yield {
            "title": response.xpath('//h1[@class="article-headline"]//text()').extract_first(),
            "date_published": response.xpath('//*[@itemprop="datePublished"]//time//@datetime').extract_first(),
            "body_text": body_text,
            "tickers": ticker_list
        }