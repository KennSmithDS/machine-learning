import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

# response = requests.get('https://www.prnewswire.com/sitemap-gz.xml')
# xml = response.text
# soup = BeautifulSoup(xml)
# map_tags = soup.find_all("sitemap")

import requests
import pandas as pd
import xmltodict

# response = requests.get('https://www.prnewswire.com/sitemap-gz.xml', headers=headers)
# url = "https://www.prnewswire.com/sitemap-gz.xml"
# res = requests.get(url)
# raw = xmltodict.parse(res.text)

# data = [[r["loc"]] for r in raw["sitemapindex"]["sitemap"]]
# print("Number of sitemaps:", len(data))
# df = pd.DataFrame(data, columns=["links"])

# df.to_csv('xml_sitemap.csv', index=False)

df = pd.read_csv('xml_sitemap.csv')
print(df.head())

