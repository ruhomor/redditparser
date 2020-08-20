from scrapy import Spider, Request, FormRequest
from reddit.items import RedditPost
from reddit import pipelines


class RedditSpider(Spider):
    name = "reddit"
    allowed_domains = ["reddit.com"]
    start_urls = ["https://www.reddit.com/login/"]

    def parse(self, response): # login function
        csrf_token = response.xpath("//input[@name='csrf_token']/@value").extract_first()
        print("TOKEN------------")
        print(csrf_token)
        print("TOKEN------------")
        yield FormRequest.from_response(response,
                                         formdata={"csrf_token": csrf_token,
                                                   "username": "belkbe1ka",
                                                   "password": "be1kabe1ka",
                                                   "dest": "https://www.reddit.com/"},
                                         callback=self.after_login)

    def after_login(self, response): # creates request for each subreddit to crawl

        subreddits = ["meme",
                      "dankmemes",
                      "PoliticalHumor",
                      "Anarcho_Capitalism",
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


