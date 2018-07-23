# -*- coding: utf-8 -*-
import scrapy
import urllib
from scrapy.http.request import Request


class AllreviewsSpider(scrapy.Spider):
    name = 'allReviews'
    # allowed_domains = ['zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews']
    # start_urls = ['https://www.zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews/']

    def parse(self, response):
        pass

    def start_requests(self):
        request = Request(url='https://8f2b7358.ngrok.io',callback=self.parse_response)
        query = 'Burger King,Cannaught Place'
        query = urllib.parse.quote_plus(query)
        # request = Request(
        #     url="https://www.zomato.com/webapi/handlers/Search/index.php?entity_type=city&entity_id=1&type=keyword&search_bar=1&query=" +
        #         query + "&without_html=true&zpwa=true",
        #     callback=self.parse_response
        # )

        yield request

    def parse_response(self, response):
        self.logger.info(response)
        pass
