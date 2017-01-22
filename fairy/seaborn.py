#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 
# 
import MySQLdb
import sys
import datetime
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 打开数据库连接
db = MySQLdb.connect("localhost","root","","fairy",charset='utf8')

cursor = db.cursor()

sql="SELECT l.USERNAME,count(*) as c FROM t_changelist l GROUP BY l.USERNAME"

df = pd.read_sql(sql,db)

#sns.distplot(df['c'],bins=16,hist=True,kde_kws={"shade": True})
#sns.plt.show()

#sns.kdeplot(df['c'],shade=True)
#sns.plt.show()

sql = "select l.ID,l.updated_at from t_changelist l"
df = pd.read_sql(sql,db)
print df
