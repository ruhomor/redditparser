from scrapy import Spider, Request
from reddit.items import RedditPost
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
            yield request

    def parse_subreddit(self, response):
        meme = RedditPost()

        post_wrapper = response.xpath("//div[@class = 'rpBJOHq2PR60pnwJlUyP0']")
        for post in post_wrapper.xpath("./div"):
            print("woah post") # debug
            meme["title"] = post.xpath(".//h3[@class='_eYtD2XCVieq6emjKBH3m']/text()").extract()
            meme["author"] = None # doesn't load for some unknown reason
            meme["date"] = post.xpath(".//a[@class='_3jOxDPIQ0KaOWpzvSQo-1s']/text()").extract()
            meme["link"] = post.xpath(".//a[@data-click-id='comments']/@href").extract()

            yield meme


