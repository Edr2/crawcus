# -*- coding: utf-8 -*-
import scrapy


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['developers.google.com/android/images']
    start_urls = ['https://developers.google.com/android/images']

    def parse(self, response):
        print(response.url)

        
