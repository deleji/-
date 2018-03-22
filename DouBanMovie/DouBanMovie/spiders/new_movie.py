# -*- coding: utf-8 -*-
import scrapy
from DouBanMovie.items import DoubanNewMovieItem
import json

class NewMovieSpider(scrapy.Spider):
    name = "new_movie"
    #allowed_domains = ["douban.com"]
    start_urls = ['https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=20&page_start=0']
    count = 0

    def parse(self, response):
        movies_dict = json.loads(response.body.decode('utf-8'))
        if movies_dict['subjects']:
            for movie in movies_dict['subjects']:
                item = DoubanNewMovieItem()
                item['movie_name'] = movie['title']
                item['score'] = movie['rate']
                item['movie_url'] = movie['url']
                movie_url = movie['url']
                yield scrapy.Request(movie_url,meta={'item':item},callback=self.parse_movie_detail)
            self.count += 20
            more_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=20&page_start={}'.format(self.count)
            yield scrapy.Request(more_url,callback=self.parse)
    
    def parse_movie_detail(self,response):
        item = response.meta['item']
        item['num'] = response.xpath("//div[@class='rating_sum']/a[@class='rating_people']/span/text()").extract_first()
        yield item
        