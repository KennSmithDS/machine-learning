import sqlite3

def create_title_table():
    conn = sqlite3.connect('prnews_articles.db')
    curr = conn.cursor()
    curr.execute("""DROP TABLE IF EXISTS articles""")
    curr.execute("""
        CREATE TABLE titles(
            url text,
            title text,
            crawl text
        )""")

    conn.commit()
    conn.close()

def create_article_table():
    conn = sqlite3.connect('prnews_articles.db')
    curr = conn.cursor()
    curr.execute("""DROP TABLE IF EXISTS articles""")
    curr.execute("""
        CREATE TABLE articles(
            url text,
            title text,
            body text,
            date text,
            tickers text
        )""")

    conn.commit()
    conn.close()

def item_db_check(item):
    conn = sqlite3.connect('prnews_articles.db')
    curr = conn.cursor()
    url_to_check = item['url']
    curr.execute("""SELECT url FROM articles WHERE url = ?""", (url_to_check, ))
    rows = curr.fetchall()
    if len(rows) == 0:
        return False
    else:
        print(f'Row with url {url_to_check} found in database')
        return True

# create_title_table()
# create_article_table()

items = [{"url": "https://www.prnewswire.com/news-releases/apresentamos-a-cytiva-lider-global-em-ciencias-biologicas-804499379.html"},
        {"url": "https://www.prnewswire.com/news-releases/smart-construction-sites-established-to-guarantee-that-the-venue-construction-of-world-university-games-chengdu-be-finished-on-time-301033106.html"},
        {"url": "https://www.prnewswire.com/news-releases/nitrosell-sees-a-50-400-increase-in-e-commerce-volumes-in-march-301037801.html"},
        {"url": "https://www.prnewswire.com/news-releases/banyan-medical-systems-aims-to-virtualize-1-000-patient-isolation-rooms-at-hospitals-nationwide-at-no-cost-301031881.html"}]

for item in items:
    db_check = item_db_check(item)
    print(db_check)