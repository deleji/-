# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class DoubanmoviePipeline(object):
    def process_item(self, item, spider):
        return item
    
class DoubanmovieCountryMysqlPipeline(object):
    def __init__(self):
        self.country_count = {}
    
    def process_item(self,item,spider):
        country_list = item['countries'].split()
        for country in country_list:
            if country not in self.country_count.keys():
                self.country_count[country] = 1
            else:
                self.country_count[country] +=1
        return item
    
    def open_spider(self,spider):
        self.conn = mysql.connector.connect(user='user',password='***',database='test')
        self.cursor = self.conn.cursor()
    
    def close_spider(self,spider):
        for dict_item in self.country_count.items():
            try:
                self.cursor.execute('insert into movie_country (country,count) values (%s,%s)',(dict_item[0],dict_item[1]))
            except Exception as e:
                print('Insert error',e)
                self.conn.rollback()
            else:
                self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
class ImdbMovieTxtPipeline(object):
    
    def __init__(self):
        self.file = open('chosen_movie.txt', 'w', encoding='utf-8')
        
    def process_item(self, item,spider):
        movie_name = item['movie_name']
        movie_score = float(item['score'])
        movie_time = int(item['time'][1:-1])
        rate_number = int(item['num'].replace(',',''))
        movie_introdution = item['introdution'].strip()
        
        if movie_time >= 1995 and rate_number >= 200000:
            line = "movie_name : %s ,\nmovie_score : %.1f ,\nmovie_time : %d ,\nrate_number : %d ,\nmovie_introdution : %s\n\n" % (
                movie_name,movie_score,movie_time,rate_number,movie_introdution)
            self.file.write(line)
        return item

class ImdbMovieMysqlPipeline(object):
    
    def open_spider(self,spider):
        self.conn = mysql.connector.connect(user='user',password='***',database='test')
        self.cursor = self.conn.cursor()
    
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
    
    def process_item(self,item,spider):
        movie_name = item['movie_name']
        movie_score = float(item['score'])
        movie_time = int(item['time'][1:-1])
        rate_number = int(item['num'].replace(',',''))
        movie_introdution = item['introdution'].strip()
        
        try:
            self.cursor.execute('insert into movie (name, score, time, number, introdution) values (%s, %s, %s, %s, %s)',
                                (movie_name, movie_score, movie_time,rate_number,movie_introdution))
        except Exception as e:
            print("Insert error",e)
            self.conn.rollback()
        else:
            self.conn.commit()
        return item    
    
