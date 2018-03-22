# -*- coding: utf-8 -*-
import scrapy
from DouBanMovie.items import DoubanmovieItem

class MovieSpider(scrapy.Spider):
    name = "movie_spider"
    #allowed_domains = ["https://movie.douban.com/top250"]
    start_urls = ['https://movie.douban.com/top250/']
    custom_settings = {
            'ITEM_PIPELINES':{'DouBanMovie.pipelines.DoubanmovieCountryMysqlPipeline':200,}
            }

    def parse(self, response):
        
        for movie in response.xpath('//div[@class="item"]'):
            item = DoubanmovieItem()
            item['movie_name'] = movie.xpath('.//span[@class="title"]/text()').extract_first()
            item['score'] = movie.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
            item['num'] = movie.xpath('.//div[@class="star"]/span[not(@class)]/text()').extract_first()
            item['time'] = movie.xpath('.//div[@class="bd"]/p/text()').re('\d{4}')[0]
            item['countries'] = movie.xpath('.//div[@class="bd"]/p/text()[2]').re('/[^0-9()]+/')[0].replace('\xa0','')[1:-1]
            item['quote'] = movie.xpath('.//p[@class="quote"]/span/text()').extract_first()
            yield item
        
        next_page_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
