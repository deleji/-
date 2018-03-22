# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:18:21 2018

@author: tmac
"""

import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

conn = mysql.connector.connect(user='root',password='921025hb',database='test')
cursor = conn.cursor()

cursor.execute('select * from movie_country')
rows = cursor.fetchall()

country = []
count  = []
for row in rows:
    country.append(row[0])
    count.append(row[1])

x_pos = np.arange(len(country))

plt.bar(x_pos,count)
plt.xticks(x_pos,country,ha='center')

for x,y in zip(x_pos,count):
    plt.text(x,y,y,ha='center', va='bottom')
    
plt.title('豆瓣电影250')
plt.xlabel('国家')
plt.ylabel('出现次数')

plt.show()
cursor.close()
conn.close()