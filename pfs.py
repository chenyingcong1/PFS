from datetime import datetime
import sqlite3
from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)
app.debug = True
DB_Feedback = r'.\db\feedback.db'

@app.route("/")
def home_page():
    return render_template('base.html')

@app.route("/feedback/")
def feedback():
    conn = sqlite3.connect(DB_Feedback)
    c = conn.cursor()
    sql = 'select ROWID,CategoryName from category'
    categories = c.execute(sql).fetchall()
    c.close()
    conn.close()
    return render_template('post.html',categories = categories)

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

@app.route('/admin/list/')
def feedback_list():
    conn = sqlite3.connect(DB_Feedback)
    c = conn.cursor()
    sql = 'select ROWID,* from feedback ORDER BY ROWID DESC '
    feedbacks = c.execute(sql).fetchall()
    conn.close()
    return render_template('feedback_list.html',feedback_list = feedbacks)

@app.route('/admin/list/del/<id>')
def del_list(id):
    conn = sqlite3.connect(DB_Feedback)
    c = conn.cursor()
    sql = 'delete from feedback WHERE ROWID = ?'
    c.execute(sql,(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('feedback_list'))

if __name__ == "__main__":
    app.run()
