# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class RedditPost(Item):
    link = Field()
    author = Field() # doesn't load for some unknown reason
    date = Field()
    title = Field()
    img = Field()
    pass
