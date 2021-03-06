# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider


class AmazonProductsSpider(Spider):
    name = 'amazon_products'
    allowed_domains = ['amazon.com']

    def __init__(self, brand=None, max_pages=5, outfile=None, *args, **kwargs):
        super(AmazonProductsSpider, self).__init__(*args, **kwargs)
        self.brand = brand
        self.max_pages = int(max_pages)
        self.outfile=outfile
        if not self.brand:
            raise Exception("missing brand")
        if not self.outfile:
            self.outfile = '{0}.csv'.format(self.brand)
        self.start_urls = ['https://www.amazon.com/s?k=Shoe&bbn=7147440011&rh=n%3A7141123011%2Cn%3A7147440011%2Cp_89%3A{0}'.format(self.brand)]

    def parse(self, response):
        for product in response.css('div[data-asin]'):
            yield {
                    'brand': self.brand,
                    'product_name': product.css('a.a-link-normal.a-text-normal span.a-text-normal::text').extract_first(),
                    'product_id': product.attrib['data-asin']
            }

            next_page = response.css('.a-last > a::attr(href)').extract_first()
            self.max_pages = self.max_pages - 1
            if next_page is not None and self.max_pages > 0:
                yield response.follow(next_page, callback=self.parse)

