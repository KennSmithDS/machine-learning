# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class PrnewsPipeline:

    def __init__(self):
        self.db_connection()

    # def __del__(self):
    #     self.close_db _connection()

    def db_connection(self):
        self.conn = sqlite3.connect('prnews_articles.db')
        self.curr = self.conn.cursor()

    # def close_db _connection(self):
    #     self.conn.close()

    def item_db_check(self, item):
        url_to_check = item['url']
        self.curr.execute("""SELECT url FROM articles WHERE url = ?""", (url_to_check, ))
        rows = self.curr.fetchall()
        if len(rows) == 0:
            return False
        else:
            return True

    def insert_item_to_db(self, item):
        self.curr.execute("""INSERT INTO articles VALUES (?, ?, ?, ?, ?)""", (
            item['url'],
            item['title'],
            item['body_text'],
            item['date_published'],
            item['tickers']
        ))
        self.conn.commit()

    def process_item(self, item, spider):
        # if not self.item_db_check(item):
        self.insert_item_to_db(item)
        return item
