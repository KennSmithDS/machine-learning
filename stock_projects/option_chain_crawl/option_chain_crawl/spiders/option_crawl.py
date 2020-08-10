import scrapy
import datetime as dt
from option_chain_crawl.items import OptionChainCrawlItem

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

class OptionChainSpider(scrapy.Spider):
    name = 'optionchain'
    base_url = 'https://finance.yahoo.com/quote'

    def get_next_friday(self):
        today = dt.date.today()
        friday = today + dt.timedelta((4-today.weekday())%7)
        return friday

    def start_requests(self):
        first_url = f'{self.base_url}/{self.equity}/options?p={self.equity}&straddle=false' #date={get_next_friday()}
        self.logger.info('Returning first url to parse option expiration dates dropdown content')
        yield scrapy.Request(url=first_url, callback=self.parse_dropdown)

    def parse_dropdown(self, response):
        option_dates = response.xpath('//*[@class="Fl(start) Pend(18px) option-contract-control drop-down-selector"]')
        if option_dates is not None:
            self.logger.info('Successfully obtained dropdown content')
            for selection in option_dates.xpath('//select/option'):
                expir_date = selection.xpath('.//text()').get()
                expir_epoch = selection.xpath('.//@value').get()
                date_url = f'{self.base_url}/{self.equity}/options?p={self.equity}&date={expir_epoch}&straddle=false'
                next_page = response.urljoin(date_url)
                self.logger.info(f'Initiating crawl for expiration date {expir_date}')
                yield scrapy.Request(next_page, callback=self.parse_chain, headers=headers, meta={'expiry': expir_date})
        else:
            self.logger.info('Was not able to obtain dropdown content')
        # in order to pass extra parameters to scrapy.Request()
        # ,  meta={'filepath': filepath}

    def parse_chain(self, response):
        call_table = response.xpath('//table[@class="calls W(100%) Pos(r) Bd(0) Pt(0) list-options"]//tbody')
        put_table = response.xpath('//table[@class="puts W(100%) Pos(r) list-options"]//tbody')

        if call_table is not None:
            self.logger.info('Calls table was found')
            for row in call_table.xpath('.//tr'):
                item = dict()
                item['contract_name'] = row.xpath('.//td[1]//text()').get()
                item['last_trade'] = row.xpath('.//td[2]//text()').get()
                item['strike'] = row.xpath('.//td[3]//text()').get()
                item['last'] = row.xpath('.//td[4]//text()').get()
                item['bid'] = row.xpath('.//td[5]//text()').get()
                item['ask'] = row.xpath('.//td[6]//text()').get()
                item['change'] = row.xpath('.//td[7]//text()').get()
                item['perc_change'] = row.xpath('.//td[8]//text()').get()
                item['volume'] = row.xpath('.//td[9]//text()').get()
                item['open_interest'] = row.xpath('.//td[10]//text()').get()
                item['implied_volatility'] = row.xpath('.//td[11]//text()').get()
                item['expiration'] = response.meta['expiry']
                item['option_type'] = 'call'
                yield item
        else:
            self.logger.info('Calls table was not found')

        if put_table is not None:
            self.logger.info('Puts table was found')
            for row in put_table.xpath('.//tr'):
                item = dict()
                item['contract_name'] = row.xpath('.//td[1]//text()').get()
                item['last_trade'] = row.xpath('.//td[2]//text()').get()
                item['strike'] = row.xpath('.//td[3]//text()').get()
                item['last'] = row.xpath('.//td[4]//text()').get()
                item['bid'] = row.xpath('.//td[5]//text()').get()
                item['ask'] = row.xpath('.//td[6]//text()').get()
                item['change'] = row.xpath('.//td[7]//text()').get()
                item['perc_change'] = row.xpath('.//td[8]//text()').get()
                item['volume'] = row.xpath('.//td[9]//text()').get()
                item['open_interest'] = row.xpath('.//td[10]//text()').get()
                item['implied_volatility'] = row.xpath('.//td[11]//text()').get()
                item['expiration'] = response.meta['expiry']
                item['option_type'] = 'put'
                yield item
        else:
            self.logger.info('Puts table was not found')