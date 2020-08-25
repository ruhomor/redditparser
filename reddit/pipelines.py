# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import functools
from reddit.items import RedditPost
import pandas as pd
import psycopg2


class PipelineAppendOneByOne:  # TODO fix indices

    def __init__(self):
        self.df = pd.DataFrame(columns=["link", "author", "date", "title"])
        self.file = open('data.csv', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print("-------------------processing_an_item-------------------")
        self.df.append(dict(item), ignore_index=True).to_csv(self.file, header=False)
        return item

class WriteToPostgre:

    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'ruslan'
        password = ''  # none???
        database = 'memes'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        print("-------------------?psql?-------------------")
        self.cur.execute("insert into reddit_content(link,author,date,title) values(%s,%s,%d,%s)",(item['link'],item['author'],item['date'],item['title']))
        self.connection.commit()
        return item
