# -*- coding: utf-8 -*-
"""
Created on 13-Feb-2020

@author: hganz
"""
import scrapy
from scrapy.spiders import Spider


class AmazonReviewsSpider(Spider):
    name = 'amazon_reviews'

    def __init__(self, product_id=None, brand=None, product_name=None, max_pages=10, outfile=None, *args, **kwargs):
        super(AmazonReviewsSpider, self).__init__(*args, **kwargs)
        self.product_id = product_id
        self.brand = brand
        self.product_name = product_name
        self.max_pages = int(max_pages)
        self.outfile = outfile
        if not self.product_id:
            raise Exception("missing product_id")
        if not self.brand:
            raise Exception("missing brand")
        if not self.product_name:
            raise Exception("missing product_name")
        if not self.outfile:
            self.outfile = '{0}-{1}-{2}.csv'.format(self.brand, self.product_name, self.product_id)
        self.start_urls = ['https://www.amazon.com/product-reviews/{0}/ref=dpx_acr_txt?showViewpoints=1'.format(self.product_id)]
        
    def parse(self, response):
        for item in response.css('.a-section.review'):
            yield {
                    'brand': self.brand,
                    'product_name': self.product_name,
                    'product_id': self.product_id,
                    'review_id': item.css('div.a-section.celwidget::attr(id)').extract_first().split('-')[1],
                    'date': item.css('[data-hook="review-date"]::text').extract_first(),
                    'stars': item.css('a::attr(title)').re_first(r'^([0-9]+).*'),
                    'review_title': item.css('[data-hook="review-title"] span::text').extract_first(),
                    'review': ' '.join(item.css('[data-hook="review-body"] span::text').extract())
            }

            next_page = response.css('.a-last > a::attr(href)').extract_first()
            self.max_pages = self.max_pages - 1
            if next_page is not None and self.max_pages > 0:
                yield response.follow(next_page, callback=self.parse)
