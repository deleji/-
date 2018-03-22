# -*- coding: utf-8 -*-
import scrapy
from DouBanMovie.items import ImdbMovieItem

class ImdbTopratedSpider(scrapy.Spider):
    name = "IMDb_TopRated"
    allowed_domains = ["imdb.com"]
    start_urls = ['http://www.imdb.com/chart/top?ref_=nv_mv_250_6']

    def parse(self, response):
        
        for movie in response.xpath('//tbody[@class="lister-list"]/tr'):
            item = ImdbMovieItem()
            item['movie_name'] = movie.xpath('./td[@class="titleColumn"]/a/text()').extract_first()
            item['time'] = movie.xpath('./td[@class="titleColumn"]/span/text()').extract_first()
            item['score'] = movie.xpath('./td[@class="ratingColumn imdbRating"]/strong/text()').extract_first()
            movie_detail_url = movie.xpath('./td[@class="titleColumn"]/a/@href').extract_first()
            yield scrapy.Request(response.urljoin(movie_detail_url),meta={'item':item},callback=self.parse_movie_detail)
    
    def parse_movie_detail(self,response):
        item = response.meta['item']
        item['num'] = response.xpath('//div[@class="ratings_wrapper"]/div[@class="imdbRating"]/a/span/text()').extract_first()
        item['introdution'] = response.xpath('//div[@class="plot_summary_wrapper"]/div[1]/div[@class="summary_text"]/text()').extract_first()
        yield item
