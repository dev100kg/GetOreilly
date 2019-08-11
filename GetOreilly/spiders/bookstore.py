# -*- coding: utf-8 -*-
import scrapy
from GetOreilly.items import GetoreillyItem
import re

class BookstoreSpider(scrapy.Spider):
    name = 'bookstore'
    allowed_domains = ['www.ohmsha.co.jp']
    start_urls = ['https://www.ohmsha.co.jp/bookstore/?catid=70&cmid=748#dnn_ctr748_ModuleContent']

    def parse(self, response):
        prefectures_pattern = '(東京都|北海道|(?:京都|大阪)府|.{2,3}県)*'
        for bookstore in response.css('.ViewProductList .storeBox'):
            yield GetoreillyItem(
                書店名称 = bookstore.css('H3::text').get(),
                郵便番号 = bookstore.css('.firstLine .post::text').get(),
                住所 = bookstore.css('.firstLine .address::text').get(),
                電話番号 = bookstore.css('.secondLine .tel .spTel::text').get(),
                url = bookstore.css('.secondLine .shopMapBtn span a.externalLink::attr(href)').get(),
                都道府県 = re.match(prefectures_pattern, bookstore.css('.firstLine .address::text').get()).group(),
                )
        next_link = response.css('#dnn_ctr747_ModuleContent div ul li.Next a::attr(href)').get()
        if next_link is None:
            print("END OF LIST")
            return
        yield scrapy.Request(next_link, callback=self.parse)