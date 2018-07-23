# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request

class AllreviewsSpider(scrapy.Spider):
    name = 'allReviews'
    # allowed_domains = ['zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews']
    # start_urls = ['https://www.zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews/']

    def parse(self, response):
        pass

    def start_requests(self):
        # request = Request(url="https://www.zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews/")
        request = Request(url='https://8f2b7358.ngrok.io')
        yield request
        