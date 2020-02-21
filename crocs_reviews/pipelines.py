# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class CrocsReviewsPipeline(object):
    def open_spider(self, spider):
        self.file = open(spider.outfile, 'a+', newline='')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        writer = csv.DictWriter(self.file, fieldnames=item.keys())
        # If file is empty, add the header line
        if self.file.tell() == 0: 
            writer.writeheader()
        # Write the current item
        writer.writerow(item)


        return item
