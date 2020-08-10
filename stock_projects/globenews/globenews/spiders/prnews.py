import scrapy
import datetime as dt
import re, os

current_dt = dt.datetime.now()
current_dt_str = current_dt.strftime('%Y_%m_%d_%H_%M_%S')
base_url = 'https://www.globenewswire.com/'

cookies = [{
    '__utmc': '202784462',
    '__utmz': '202784462.1528781417.4.2.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided)',
    'ASP.NET_SessionId': '0x4wpdo5nkerk02im3uuyhqi',
    '__pnrculture': 'en-US',
    'GNWTracker': '337e8809-2cad-4668-9eb2-0d35792f123a',
    '__RequestVerificationToken_Lw__': 'vQhDuUP8SlEXWlyfKo7W+u3gMpnisNMFryv8Wg+sDj1ZYpDqyBxutA8lHFEtkPuLT7XDCYCrc6ktgJ4/a7kTsPS10NVuggx0HbyCwAAZHsVx4uyT06Q2nGcUN9NUfrUZ9GicWA==',
    '__utma': '202784462.593866152.1524205181.1528781417.1530375868.5',
    '__utmt': '1',
    '__utmb': '202784462.1.10.1530375868',
},

{
    '__utmc': '202784462',
    '__utmz': '202784462.1528781417.4.2.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided)',
    'ASP.NET_SessionId': '0x4wpdo5nkerk02im3uuyhqi',
    '__pnrculture': 'en-US',
    'GNWTracker': '337e8809-2cad-4668-9eb2-0d35792f123a',
    '__RequestVerificationToken_Lw__': 'vQhDuUP8SlEXWlyfKo7W+u3gMpnisNMFryv8Wg+sDj1ZYpDqyBxutA8lHFEtkPuLT7XDCYCrc6ktgJ4/a7kTsPS10NVuggx0HbyCwAAZHsVx4uyT06Q2nGcUN9NUfrUZ9GicWA==',
    '__utma': '202784462.593866152.1524205181.1530378754.1530394024.7',
    '__utmt': '1',
    '__atuvc': '7^%^7C26',
    '__atuvs': '5b37f5b064867ed6006',
    '__utmb': '202784462.19.10.1530394024',
},

{
    '__utmc': '202784462',
    '__utmz': '202784462.1528781417.4.2.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided)',
    'ASP.NET_SessionId': '0x4wpdo5nkerk02im3uuyhqi',
    '__pnrculture': 'en-US',
    'GNWTracker': '337e8809-2cad-4668-9eb2-0d35792f123a',
    '__RequestVerificationToken_Lw__': 'vQhDuUP8SlEXWlyfKo7W+u3gMpnisNMFryv8Wg+sDj1ZYpDqyBxutA8lHFEtkPuLT7XDCYCrc6ktgJ4/a7kTsPS10NVuggx0HbyCwAAZHsVx4uyT06Q2nGcUN9NUfrUZ9GicWA==',
    '__utma': '202784462.593866152.1524205181.1530378754.1530394024.7',
    '__utmt': '1',
    '__atuvc': '8^%^7C26',
    '__atuvs': '5b37f5b064867ed6007',
    '__utmb': '202784462.25.10.1530394024',
}]

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
                yield scrapy.Request(article_crawl, callback=self.parse_news_article, cookies=cookies, headers=headers)

        next_path = response.xpath('//li[@class="ui-html-pager-next"]//a//@href').extract_first()
        next_page = base_url + next_path
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, cookies=cookies, headers=headers)

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