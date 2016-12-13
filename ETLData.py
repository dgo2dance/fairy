#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import sys
import datetime
import time

# 打开数据库连接
db = MySQLdb.connect("localhost","root","","fairy",charset='utf8')

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS T_EMPLOYEE")

# 创建数据表SQL语句
sql = """CREATE TABLE T_EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""

#cursor.execute(sql)


# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS T_REMHISTORY")

# 创建数据表SQL语句
sql2 = """CREATE TABLE T_REMHISTORY (
         ID int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
         STOCK_NAME  CHAR(20) NOT NULL,
         stock_symbol varchar(20) NOT NULL,
         CON  INT,
         NEXTDAYRATE FLOAT,
         CREATE_TIME DATETIME,
         UPDATE_TIME DATETIME,
         PRIMARY KEY (ID)
        )"""

cursor.execute(sql2)




# SQL 查询语句
# sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)
sql = "SELECT L.STOCK_NAME,L.STOCK_SYMBOL,COUNT(DISTINCT L.USERNAME) AS con FROM (SELECT * FROM fairy.t_changelist t WHERE t.TARGET_WEIGHT > t.PREV_WEIGHT_AJJUSTED AND t.updated_at > '2016-12-13' AND t.sign in  ('WEEK','MONTH')) L GROUP BY L.STOCK_NAME,L.STOCK_SYMBOL ORDER BY con DESC"
print sql
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      stock_name = row[0]
      stock_symbol = row[1]
      con = row[2]
      # 打印结果
      print "stock_name=%s,con=%s" % \
      (stock_name, con)
      # SQL 插入语句
      currentTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
      sql = "INSERT INTO t_remHistory(stock_name, stock_symbol, con,CREATE_TIME,update_time) \
      VALUES ('%s', '%s','%d','%s','%s')" % (stock_name,stock_symbol, con,currentTime,currentTime)
      cursor.execute(sql)
      db.commit()

except :
   print "Error: unable to fecth data"
   print 	sys.exc_info() 

# 关闭数据库连接
db.close()