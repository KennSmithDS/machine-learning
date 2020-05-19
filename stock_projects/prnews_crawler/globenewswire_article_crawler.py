import requests
import numpy as np
import sys
from datetime import datetime
import time
import os
import re
import logging
import pandas as pd
from bs4 import BeautifulSoup

today = datetime.today().strftime('%m/%d/%Y')

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

proxy = {
    'Http': 'http://ba1e790ec7694f3dab119531c59efde3:@klsCrawl.crawlera.com:8010'
}

def setup_logger(log_dir=None,
                 log_file=None,
                 log_format=logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
                 log_level=logging.INFO):
    # Get logger
    logger = logging.getLogger('')
    # Clear logger
    logger.handlers = []
    # Set level
    logger.setLevel(log_level)
    # Setup screen logging (standard out)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(log_format)
    logger.addHandler(sh)
    # Setup file logging
    if log_dir and log_file:
        fh = logging.FileHandler(os.path.join(log_dir, log_file))
        fh.setFormatter(log_format)
        logger.addHandler(fh)

    return logger

def getRandomCookie(cookies):
    return np.random.choice(cookies)

def openUrl(url, header):
    try:
        temp_cookie = getRandomCookie(cookies)
        response = requests.get(url, headers=header, cookies=temp_cookie, proxies=proxy, verify=False)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))
        pass

def findReleaseLinks(soup, today):
    try:
        # create blank lists for links, titles, dates and company names
        releases = pd.DataFrame()
        links = []
        titles = []
        dates = []
        companies = []

        # find all header containers with article links
        results = soup.find_all('div', class_='results-link')
        for result in results:
            # find company names
            company_p = result.find_all('p', class_='company-title')
            if company_p:
                companies.append(company_p[0].text)

            # find links and article titles
            link_h = result.find_all('h1', class_='post-title16px')
            for container in link_h:
                link_a = container.find('a', href=True)
                if link_a.text:
                    links.append(link_a['href'])
                    titles.append(link_a.text)

            # find article release date
            date_p = result.find_all('p', class_='post-metadata')
            if date_p:
                if 'hours' in date_p[0].text or 'hour' in date_p[0].text or 'minutes' in date_p[0].text or 'minute' in date_p[0].text:
                    dates.append(today)
                else:
                    date_clean = date_p[0].text.lstrip('\n').strip().replace('photo-release', '')
                    date = datetime.strptime(date_clean, '%B %d, %Y').strftime('%m/%d/%Y')
                    dates.append(date)

        releases['links'] = links
        releases['titles'] = titles
        releases['dates'] = dates
        releases['companies'] = companies
        print(releases.head())
        return releases

    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))

def articleCheck():
    # account_dif = soup.find('div', class_='hero-landing-download')
    pass

def saveFile(soup, file_num):
    os.chdir('C://Users//kenns//PycharmProjects//StockFeeder//globenewswire_articles')
    # title.replace(' ', '_')
    file_name = str(file_num) + '.html'
    # if len(file_name) > 150:
    #     file_name = file_name[:151]
    # else:
    #     pass
    with open(file_name, 'w') as file:
        file.write(str(soup))

if __name__ == "__main__":

    # Setup directories
    data_dir = 'data'
    logging_dir = 'logs'
    time_date = datetime.now()
    string_date = time_date.strftime("%Y%m%d_%H%M%S")

    # Setup Logging
    logging_level = logging.INFO
    if not os.path.exists(logging_dir):
        os.makedirs(logging_dir)
    logging_file = 'globe_news_wire_article_crawler_{}.log'.format(string_date)
    log = setup_logger(logging_dir, logging_file, log_level=logging_level)

    try:

        log.info('Initiating program...')
        program_start = time.time()

        # open each page in news_release site for a given range
        root_url = 'http://www.globenewswire.com'
        article_num = 1
        page_range = np.arange(2)

        for i in range(len(page_range)):
            release_start = time.time()
            releases_url = 'http://www.globenewswire.com/Index?page=' + str(i+1) + '#pagerPos'
            release_soup = openUrl(releases_url, headers)
            saveFile(release_soup, ('r_' + str(i+1)))
            page_releases = findReleaseLinks(release_soup, today)
            release_end = time.time()
            log.info('Fetching release page {a} took {b} seconds.'.format(a=str(i+1), b=str(release_end - release_start)))

            # for each link found, open separate request
            for link in page_releases['links']:
                article_start = time.time()
                article_url = root_url + link
                log.info('Fetching html for article at URL: ' + article_url)
                article_soup = openUrl(article_url, headers)
                if article_soup:
                    title_h = article_soup.find_all('h1', class_='article-headline')
                    title = title_h[0].text
                    log.info('Article title found at URL: {}'.format(title))
                    saveFile(article_soup, article_num)
                    article_num += 1
                    article_end = time.time()
                    log.info('Fetching article article took {} seconds.'.format(str(article_end - article_start)))
                else:
                    pass

            # check to see if subscription is required to view
            # only applied when opening HTML link for article
            # save html text to file in archive folder

        program_end = time.time()
        log.info('Program run time at completion was {} seconds total.'.format(str(program_end - program_start)))

    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))
        pass