# -*- coding: utf-8 -*-
import scrapy
import urllib
import random
from scrapy.http.request import Request


class AllreviewsSpider(scrapy.Spider):
    name = 'allReviews'
    # allowed_domains = ['zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews']
    # start_urls = ['https://www.zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews/']

    def __init__(self, *args, **kwargs):
        self.userAgents = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0)","Mozilla/5.0 (Windows NT 6.1; Win64; x64)","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko)","Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko)",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko)","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko)","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko)","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko)","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko)"]
    def parse(self, response):
        pass

    def start_requests(self):
        
        headers = {'user-agent':random.SystemRandom().choice(self.userAgents)}
        request = Request(url='https://8f2b7358.ngrok.io',
                          callback=self.parse_response, dont_filter=True,headers=headers)
        query = 'Burger King,Cannaught Place'
        query = urllib.parse.quote_plus(query)
        # request = Request(
        #     url="https://www.zomato.com/webapi/handlers/Search/index.php?entity_type=city&entity_id=1&type=keyword&search_bar=1&query=" +
        #         query + "&without_html=true&zpwa=true",
        #     callback=self.parse_response
        # )

        yield request

    def parse_response(self, response):
        headers = {'user-agent':random.SystemRandom().choice(self.userAgents)}
        self.logger.info(response)
        yield Request(url='https://8f2b7358.ngrok.io', headers=headers, dont_filter=True)
        pass
