import sqlite3
from flask import g
import os
DB_Feedback = os.path.realpath('./db/feedback.db')


def make_dict(cursor,row):
    return dict(cursor.description[i][0] for i, value in enumerate(row))

def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = sqlite3.connect(DB_Feedback)
        g._database = db #把连接变量放入g缓存
    return db

def execute_sql(sql, prms=()):
    c = get_db().cursor()
    c.execute(sql, prms)
    c.connection.commit()

def query_sql(sql, prms=(),one = False):
    c = get_db().cursor()
    result = c.execute(sql,prms).fetchall()
    c.close()
    return result[0] if one else result