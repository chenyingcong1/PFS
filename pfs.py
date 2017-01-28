from datetime import datetime
import sqlite3
import pymysql
from flask import Flask,render_template,request,redirect,url_for,g

app = Flask(__name__)
app.debug = True
DB_Feedback = r'.\db\feedback.db'
SQL_Feedback = ''

def make_dict(cursor,row):
    return dict(cursor.description[i][0] for i, value in enumerate(row))

def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = sqlite3.connect(DB_Feedback)
        g._database = db #把连接变量放入g缓存
    return db



@app.route("/")
def home_page():
    return render_template('base.html')

@app.route("/url_list/")
def url_table():
    return render_template('url_list.html')

@app.route("/feedback/")
def feedback():
    conn = sqlite3.connect(DB_Feedback)
    c = conn.cursor()
    sql = 'select ROWID,CategoryName from category'
    categories = c.execute(sql).fetchall()
    c.close()
    conn.close()
    return render_template('post.html',categories = categories)
#上传问题列表
@app.route('/post_feedback/', methods=['POST'])
def post_feedback():
    #如果当前请求的方法为POST
    if request.method == 'POST':
        # 获取表单值
        subject = request.form['subject']
        categoryid = request.form.get('category', 1)
        feedback = request.form.get('feedback')
        process = request.form.get('process')
        phone = request.form.get('phone')
        body = request.form.get('body')
        state = request.form.get('state')
        reply = request.form.get('reply')
        releasetime = datetime.now()


        conn = sqlite3.connect(DB_Feedback)
        c = conn.cursor()
        sql = "insert into feedback(Subject,CategoryID,Feedback,Process,Phone,Body,State,Reply,ReleaseTime) values (?,?,?,?,?,?,?,?,?)"
        c.execute(sql,(subject,categoryid,feedback,process,phone,body,state,reply,releasetime))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback'))

@app.route('/test/')
def test():
    return 'test'
# 管理员列表编辑页
@app.route('/admin/list/')
def feedback_list():
    conn = sqlite3.connect(DB_Feedback)
    c = conn.cursor()
    sql = 'select ROWID,* from feedback ORDER BY ROWID DESC '
    feedbacks = c.execute(sql).fetchall()
    conn.close()
    return render_template('feedback_list.html',feedback_list = feedbacks)
# 删除列表
@app.route('/admin/list/del/<id>')
def del_list(id):
    conn = sqlite3.connect(DB_Feedback)
    c = conn.cursor()
    sql = 'delete from feedback WHERE ROWID = ?'
    c.execute(sql,(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('feedback_list'))
# 编辑列表
@app.route('/admin/list/edit/<id>')
def edit_list(id):
    conn = sqlite3.connect(DB_Feedback)
    c = conn.cursor()

    sql = 'select rowid,CategoryName from category'
    categories = c.execute(sql).fetchall()

    sql = 'select rowid,* from feedback WHERE ROWID = ?'
    current_feedback = c.execute(sql,(id,)).fetchone()
    c.close()
    conn.close()
    return render_template('edit.html',categories = categories, item = current_feedback)
#保存编辑列表
@app.route('/admin/list/save_edit/',methods=['POST'])
def save_edit():
    if request.method == 'POST':
        subject = request.form.get('subject')
        rowid = request.form.get('rowid',None)
        categoryid = request.form.get('category',1)
        feedback = request.form.get('feedback')
        process = request.form.get('process')
        phone = request.form.get('phone')
        body = request.form.get('body')
        state = request.form.get('state')
        releasetime = request.form.get('releasetime')

        conn = sqlite3.connect(DB_Feedback)
        c = conn.cursor()
        sql = """update feedback set
                                Subject = ?,
                                categoryid = ?,
                                feedback = ?,
                                process = ?,
                                phone = ?,
                                body = ?,
                                state = ?,
                                releasetime = ?
                        where rowid = ?
        """
        c.execute(sql,(subject,categoryid,feedback,process,phone,body,state,releasetime,rowid))
        conn.commit()
        conn.close()
        return redirect(url_for('feedback_list'))
#查看详细列表
@app.route('/admin/list/search_list/<id>')
def search_list(id):
    conn = sqlite3.connect(DB_Feedback)
    c = conn.cursor()
    sql = 'select rowid,CategoryName from category'
    categories = c.execute(sql).fetchall()

    sql = 'select rowid,* from feedback WHERE ROWID = ?'
    current_feedback = c.execute(sql, (id,)).fetchone()
    c.close()
    conn.close()
    return render_template('search.html', categories=categories, item=current_feedback)



if __name__ == "__main__":
    app.run()
