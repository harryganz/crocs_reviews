# -*- coding: utf-8 -*-
"""
Created on 13-Feb-2020

@author: hganz
"""
import scrapy
from scrapy.spiders import Spider


class AmazonReviewsSpider(Spider):
    name = 'amazon_reviews'

    def __init__(self, product_id=None, *args, **kwargs):
        super(AmazonReviewsSpider, self).__init__(*args, **kwargs)
        self.product_id = product_id
        if not self.product_id:
            raise Exception("missing product_id")
        self.start_urls = ['https://www.amazon.com/product-reviews/{0}/ref=dpx_acr_txt?showViewpoints=1'.format(self.product_id)]
        
    def parse(self, response):
        for item in response.css('.a-section.review'):
            yield {
                    'product_id': self.product_id,
                    'review_id': item.css('div.a-section.celwidget::attr(id)').extract_first().split('-')[1],
                    'date': item.css('[data-hook="review-date"]::text').extract_first(),
                    'stars': item.css('a::attr(title)').extract_first(),
                    'review_Title': item.css('[data-hook="review-title"]::text').extract_first(),
                    'review': ' '.join(item.css('span.review-text::text').extract())
            }

            next_page = response.css('.a-last > a::attr(href)').extract_first()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
