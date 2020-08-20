from scrapy import Spider, Request, FormRequest
from reddit.items import RedditPost
from urllib.parse import urlencode
import json
from reddit import pipelines


class RedditSpider(Spider):
    name = "reddit"
    allowed_domains = ["reddit.com"]
    start_urls = ["https://www.reddit.com/login/"]
    subreddits = ["meme",
                  "dankmemes",
                  "PoliticalHumor",
                  "Anarcho_Capitalism",
                  "ProgrammerAnimemes"]
    scroll_urls = {e: f"https://gateway.reddit.com/desktopapi/v1/subreddits/{e}?" for e in subreddits}
    params = {e: {"rtj": "only",
                  "redditWebClient": "web2x",
                  "app": "web2x-client-production",
                  "allow_over18": "1",  # adult content lol
                  "include": "prefsSubreddit",
                  "after": "t3_icgvnd",
                  "dist": "1",
                  "layout": "card",
                  "sort": "hot",
                  "geo_filter": "RU"
                  } for e in subreddits}

    def parse(self, response):  # login function
        csrf_token = response.xpath("//input[@name='csrf_token']/@value").extract_first()
        print("TOKEN------------LOGIN")
        print(csrf_token)
        print("TOKEN------------LOGIN")
        yield FormRequest.from_response(response,
                                        formdata={"csrf_token": csrf_token,
                                                  "username": "belkbe1ka",
                                                  "password": "be1kabe1ka",
                                                  "dest": "https://www.reddit.com/"},
                                        callback=self.after_login)

    def after_login(self, response):  # creates request for each subreddit to crawl
        for subreddit in self.subreddits:
            print("----------{}---------".format(subreddit))  # debug
            url = self.scroll_urls[subreddit] + urlencode(self.params[subreddit])
            yield Request(url, callback=self.subreddit_scroll)

    def subreddit_scroll(self, response):
        json_data = json.loads(response.text)
        subreddit = json_data["subreddits"][str(list(json_data["subreddits"].keys())[0])]["name"]  # Stupid as f

        self.params[subreddit]["after"] = json_data["token"]
        self.params[subreddit]["dist"] = json_data["dist"]

        for i in range(0, 3):  # scrolls
            url = self.scroll_urls[subreddit] + urlencode(self.params[subreddit])
            print("-----------SCROLLING-----------")  # debug
            yield Request(url, callback=self.parse_subreddit)

    def parse_subreddit(self, response):
        print("---------PARSING_PAGE----------")  # debug
        meme = RedditPost()

        post_wrapper = response.xpath("//div[@class = 'rpBJOHq2PR60pnwJlUyP0']")
        for post in post_wrapper.xpath("./div"):  # TODO skip parsed posts
            print("----------!Woah Post!----------")  # debug
            meme["title"] = post.xpath(".//h3[@class='_eYtD2XCVieq6emjKBH3m']/text()").extract()
            meme["author"] = None  # doesn't load for some unknown reason
            meme["date"] = post.xpath(".//a[@class='_3jOxDPIQ0KaOWpzvSQo-1s']/text()").extract()
            meme["link"] = post.xpath(".//a[@data-click-id='comments']/@href").extract()
            yield meme