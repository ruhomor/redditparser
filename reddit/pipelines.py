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
