# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmovieItem(scrapy.Item):
    
    movie_name = scrapy.Field()
    score = scrapy.Field()
    num = scrapy.Field()
    time = scrapy.Field()
    quote = scrapy.Field()
    countries = scrapy.Field()
    
class DoubanNewMovieItem(scrapy.Item):
    movie_name = scrapy.Field()
    movie_url = scrapy.Field()
    score = scrapy.Field()
    num = scrapy.Field()

class ImdbMovieItem(scrapy.Item):
    movie_name = scrapy.Field()
    score = scrapy.Field()
    num = scrapy.Field()
    time = scrapy.Field()
    introdution = scrapy.Field()