# -*- coding: utf-8 -*-
"""
Created on Mon May 15 17:25:48 2023

@author: Lenovo
"""

import pandas as pd
import numpy as np

f = open(r'D:\风控\zodiac1.csv', encoding='utf-8')
#excel或其他文件储存最好选用CSV UTF-8这个格式，好打开
ft_zodiac = pd.read_csv(f)  
ft_zodiac.head()


#查一下数据集有没有重复的order_id
len(set(ft_zodiac.order_id))
len(ft_zodiac.order_id)


l = open(r'D:\风控\label.txt')
zodiac_label=pd.read_csv(l)
ft_label = zodiac_label[zodiac_label['label'] != 2]
ft_label.head()


data = pd.merge(ft_label,ft_zodiac,on = 'order_id',how = 'inner')
data.head()
#overdue_days历史逾期天数

zodiac_list = set(data.zodiac)  
#set()创建无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等

label_list = set(data.label)
chinese_zodiac_list = set(data.chinese_zodiac)
zodiac_list
chinese_zodiac_list

#计算星座坏账率
zodiac_badrate = {}
for x in zodiac_list:
    
    a = data[data.zodiac == x]
    
    bad = a[a.label == 1]['label'].count()
    good = a[a.label == 0]['label'].count()
    
    zodiac_badrate[x] = bad/(bad+good)
    
    
f = zip(zodiac_badrate.keys(),zodiac_badrate.values())
f = sorted(f,key = lambda x : x[1],reverse = True )
zodiac_badrate = pd.DataFrame(f)
zodiac_badrate.columns = pd.Series(['星座','badrate'])
zodiac_badrate


#安装老版pychart line
#绘图：星座-坏账率折线图
from pyecharts import Line
x = zodiac_badrate['星座']
y = zodiac_badrate['badrate']
line = Line('星座')
line.add(1,x,y)
#一般差距几倍以上才会有效，途中这种差距很小，表明星座和坏账没什么关系

#计算生肖坏账率
chinese_zodiac_badrate = {}
for x in chinese_zodiac_list:
    
    a = data[data.chinese_zodiac == x]
    
    bad = a[a.label == 1]['label'].count() #选取每个星座对应的label这一列的坏人个数
    good = a[a.label == 0]['label'].count()
    
    chinese_zodiac_badrate[x] = bad/(bad+good)
    
    
f = zip(chinese_zodiac_badrate.keys(),chinese_zodiac_badrate.values()) #zip()将对象中对应的元素打包成一个个元组
f = sorted(f,key = lambda x : x[1],reverse = True )#对badrate进行排序
chinese_zodiac_badrate = pd.DataFrame(f)
chinese_zodiac_badrate.columns = pd.Series(['生肖','badrate'])
chinese_zodiac_badrate

#绘图：生肖-坏账率折线图
x = chinese_zodiac_badrate['生肖']
y = chinese_zodiac_badrate['badrate']
line = Line('生肖')
line.add(1,x,y)