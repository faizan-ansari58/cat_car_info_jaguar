# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MainItem(scrapy.Item):
    model_title = scrapy.Field()
    model_link = scrapy.Field()
    model_image = scrapy.Field()
    parameter_title = scrapy.Field()
    parameter_link = scrapy.Field()
    group_title = scrapy.Field()
    group_link = scrapy.Field()
    subgroup_title = scrapy.Field()
    link_no = scrapy.Field()
    subgroup_link = scrapy.Field()
    

    
    