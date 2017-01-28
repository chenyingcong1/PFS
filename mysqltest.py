from datetime import datetime
import sqlite3
from flask import Flask,render_template,request,redirect,url_for,g

app = Flask(__name__)
app.debug = True
DATABASE_URL = r'.\db\feedback.db'

#将游标获取的tuple根据数据库列表转换为dict
def make_dicts(cursor,row):
    return dict((cursor.description[i][0],value) for i,value in enumerate(row))

#获取（建立数据库连接）
sql = 'select f.ROWID,f.*,c.CategoryName from feedback f INNER JOIN category c ON c.ROWID = f.CategoryID ORDER BY f.ROWID DESC '
db = sqlite3.connect(DATABASE_URL)
db.row_factory = make_dicts
c = db.cursor()
result = c.execute(sql).fetchall()
print(result)
# for results in result:
#     print(results)
# print(result)

# #执行sql语句不返回数据结果
# def execute_sql(sql,prms=()):
#     c = get_db().cursor()
#     c.execute(sql,prms)
#     c.connection.commit()
# #执行用于选择数据的sql语句
# def query_sql(sql,prms =(),one=False):
#     c = get_db().cursor()
#     result = c.execute(sql,prms).fetchall()
#     c.close()
#     return (result[0] if result else None) if one else result
# sql = 'select ROWID,CategoryName from category'
# if __name__ == '__main__':
#
# categories = query_sql(sql)