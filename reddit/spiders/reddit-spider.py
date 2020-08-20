from scrapy import Spider, Request, FormRequest
from reddit.items import RedditPost
from urllib.parse import urlencode
import json
from reddit import pipelines


class RedditSpider(Spider):
    name = "reddit"
    number_of_scrolls = 1  # number of scrolls + 1: 1 = 2 scrolls; 3 = 4 scrolls
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
    scrolls = {e:0 for e in subreddits}

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
        url = self.scroll_urls[subreddit] + urlencode(self.params[subreddit])

        print("--++--++--++--DIST_{}-{}++--++--++--".format(json_data["dist"], subreddit))  # scroll debug
        if self.scrolls[subreddit] > self.number_of_scrolls:  # number of scrolls
            yield Request(url, callback=self.parse_subreddit)
        else:
            print("-----------SCROLLING-----------")  # debug
            self.scrolls[subreddit] += 1
            yield Request(url, callback=self.subreddit_scroll)


    def parse_subreddit(self, response):
        print("---------PARSING_PAGE----------")  # debug
        meme = RedditPost()

        json_data = json.loads(response.text)
        for post in json_data["postIds"]:
            print("----------!Woah Post!----------")
            meme["title"] = json_data["posts"][post]["title"]
            meme["author"] = json_data["posts"][post]["author"]
            meme["link"] = json_data["posts"][post]["permalink"]
            meme["date"] = json_data["posts"][post]["created"]
            yield meme
