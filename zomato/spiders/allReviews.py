# -*- coding: utf-8 -*-
import scrapy


class AllreviewsSpider(scrapy.Spider):
    name = 'allReviews'
    # allowed_domains = ['zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews']
    # start_urls = ['https://www.zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews/']
    start_urls = ['https://a2fdd6c0.ngrok.io/']

    def parse(self, response):
        pass
