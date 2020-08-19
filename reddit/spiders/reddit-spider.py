from scrapy import Spider, Request
from reddit.items import RedditItem
from reddit import pipelines


class RedditSpider(Spider):
    name = "reddit"

    def start_requests(self):
        subreddits = ["meme",
                       "dankmemes",
                       "PoliticalHumor",
                      "ProgrammerAnimemes"]

        for subreddit in subreddits:
            url = f"https://www.reddit.com/r/{subreddit}/"
            request = Request(url, callback=self.parse_subreddit)
            request.meta["subreddit"] = subreddit
            yield request

    def parse_subreddit(self, response):
        meme = RedditPost()

        post_wrapper = response.xpath("//div[@class = 'rpBJOHq2PR60pnwJlUyP0']")
        for post in post_wrapper.xpath("/div")
        meme["origin"] = response.meta["subreddit"]
        meme["author"] = post.xpath["//*[@id='t3_ic9uxz']/div[2]/div[1]/div/div[1]/div/a"]


