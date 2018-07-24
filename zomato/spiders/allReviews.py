# -*- coding: utf-8 -*-
import scrapy
import urllib
import random
from scrapy.http.request import Request
import json
from bs4 import BeautifulSoup
import csv
import os.path



class AllreviewsSpider(scrapy.Spider):
    name = 'allReviews'
    # allowed_domains = ['zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews']
    # start_urls = ['https://www.zomato.com/ncr/bukhara-itc-maurya-chanakyapuri-new-delhi/reviews/']

    def __init__(self, *args, **kwargs):
        self.userAgents = ["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0)", "Mozilla/5.0 (Windows NT 6.1; Win64; x64)", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko)", "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko)",
                           "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko)", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko)",
                           "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko)", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko)"]
        self.entity_id = None
        self.page_more = 1
        self.more_reviews = []
        self.sno = 0

    def parse(self, response):
        pass

    def start_requests(self):

        headers = {'user-agent': random.SystemRandom().choice(self.userAgents)}
        # request = Request(url='https://8f2b7358.ngrok.io',
        #                   callback=self.parse_response, dont_filter=True,headers=headers)
        query = 'Burger King,Cannaught Place'
        query = urllib.parse.quote_plus(query)
        # request = Request(
        #     url="https://www.zomato.com/webapi/handlers/Search/index.php?entity_type=city&entity_id=1&type=keyword&search_bar=1&query=" +
        #         query + "&without_html=true&zpwa=true",
        #     callback=self.parse_response, headers=headers
        # )

        yield Request(
            url="https://www.zomato.com/webapi/handlers/Search/index.php?entity_type=city&entity_id=1&type=keyword&search_bar=1&query=" +
                query + "&without_html=true&zpwa=true",
            callback=self.parse_response, headers=headers
        )

    def parse_response(self, response):
        results = (json.loads(response.text))['results']
        for result in results:
            if result['entity_type'] == 'restaurant':
                print(result['entity_id'])
                self.entity_id = result['entity_id']
                break
        headers = {'user-agent': random.SystemRandom().choice(self.userAgents)}
        self.page_more = 1
        page_no = 0
        data = {
            "entity_id": str(self.entity_id),
            "profile_action": "reviews-dd",
            "page": str(page_no),
            "limit": '5'
        }
        
        for i in range(10):
            data['page'] = str(i)
            self.logger.info(data)
            yield scrapy.FormRequest(url="https://www.zomato.com/php/social_load_more.php",
                                callback=self.parse_reviews, formdata=data, headers=headers)
        # self.logger.info(self.more_reviews)

    def parse_reviews(self, response):
        page_response = (json.loads(response.text))
        page_html = page_response['html']

        self.page_more = int(page_response['more'])
        self.logger.info('LEFT COUNT %s',page_response['left_count'])

        star_map = {
            "icon-font-level-9": "Rated 5.0",
            "icon-font-level-8": "Rated 4.5",
            "icon-font-level-7": "Rated 4.0",
            "icon-font-level-6": "Rated 3.5",
            "icon-font-level-5": "Rated 3.0",
            "icon-font-level-4": "Rated 2.5",
            "icon-font-level-3": "Rated 2.0",
            "icon-font-level-2": "Rated 1.5",
            "icon-font-level-1": "Rated 1.0",
        }
                
        soup_more=BeautifulSoup(response.text,"lxml")
        outer_containers_added=soup_more.findAll("div",{"class":"\\\"header"})
        self.logger.info('LENGTH %s',len(outer_containers_added))
        self.more_reviews = []
        for outer_container in outer_containers_added:
            more_review={}
            self.sno += 1 

            more_review["s.no"]=self.sno
            try:
                more_review["users_name"]=outer_container.find("a").contents[0].replace("\\n","").strip()
                self.logger.info(more_review['users_name'])
            except:
                more_review["users_name"]="not-found"
            try:
                more_review["users_reviews"]=outer_container.find("span",{"class":'\\\"grey-text'}).contents[0].replace("\\n","").strip().split(",")[0].strip()
            except:
                more_review["users_reviews"]="not-found"
            try:
                if len(outer_container.find("span",{"class":'\\\"grey-text'}).contents[0].replace("\\n","").strip().split(",")) == 1:
                    more_review["users_followers"] = '0 Followers'
                else:
                    more_review["users_followers"]=outer_container.find("span",{"class":'\\\"grey-text'}).contents[0].replace("\\n","").strip().split(",")[1].strip()
            except:
                more_review["users_followers"]="not-found"
            
            try:
                more_review["creation_time"]=outer_container.find("a",{"class":'\\\"grey-text\\\"'}).find("time")["datetime"].replace('\\"',"")
            except:
                more_review["creation_time"]="not-found"
            try:
                rating_div=outer_container.find("div",{"class":"\\\"rev-text"}).find("div",{"class":"\\\"ttupper"})
                #more_review["rating"]=star_map[sorted(list(rating_div.attrs.keys()))[5]]
                more_review["rating"]=star_map["icon-font-level-"+rating_div["data-iconr"].split('\\')[2][-1]]
            except:
                more_review["rating"]="not-found"
            try:
                more_review["review_text"]=outer_container.find("div",{"class":"\\\"rev-text"}).find("div",{"class":"\\\"ttupper"}).contents[0].split("\\n")[1].strip()
            except:
                more_review["review_text"]="not-found"
                
            self.more_reviews.append(more_review)
        # self.logger.info(self.more_reviews)
        writeHeader=True
        if((os.path.exists('zomato_data.csv'))):
            writeHeader=False
    
        with open('zomato_data.csv', 'a') as f:
            writer = csv.DictWriter(f, self.more_reviews[0].keys())
            if writeHeader:
                writer.writeheader()
            for more_review in self.more_reviews:
                    writer.writerow(more_review)



#SCRAPY SHELL
# data ={'entity_id': '310780',
#  'limit': '5',
#  'page': '0',
#  'profile_action': 'reviews-dd'}

# url="https://www.zomato.com/php/social_load_more.php"

# r = FormRequest(url, formdata=data,headers = {'user-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0)"})

# fetch(r)