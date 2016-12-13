#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import sys

# 打开数据库连接
db = MySQLdb.connect("localhost","root","","fairy" )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS fairy.EMPLOYEE")

# 创建数据表SQL语句
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)


# SQL 查询语句
# sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)
sql = "SELECT L.STOCK_NAME,COUNT(DISTINCT L.USERNAME) AS con FROM (SELECT * FROM fairy.t_changelist t WHERE t.TARGET_WEIGHT > t.PREV_WEIGHT_AJJUSTED AND t.updated_at > '2016-12-13' AND t.sign in  ('WEEK','MONTH')) L GROUP BY L.STOCK_NAME ORDER BY con DESC"
print sql
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      stock_name = row[0]
      con = row[1]

      # 打印结果
      print "stock_name=%s,con=%s" % \
             (stock_name, con)
except :
   print "Error: unable to fecth data"
   print 	sys.exc_info() 





# 关闭数据库连接
db.close()