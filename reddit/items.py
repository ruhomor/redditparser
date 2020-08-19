# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class RedditPost(Item):
    link = Field()
    author = Field()
    date = Field()
    text = Field()
    img_file = Field()
    vote_count = Field()
    award_count = Field()
    comment_count = Field()
    caption = Field()
    origin = Field()
    pass

class SubReddit(Item):
    name = Field()
    link = Field()
    about = Field()
    rules = Field()
    similar = Field()
    moderators = Field()
    pass
