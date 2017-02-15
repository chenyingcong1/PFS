from datetime import datetime
import sqlite3
import os
from flask import Flask,render_template,request,redirect,url_for,g,send_from_directory
from sql_info import make_dict,get_db,query_sql,execute_sql
from leave_table import make_otsheet,make_hotsheet,make_annsheet,make_bsnssheet
from flask_uploads import UploadSet, configure_uploads,patch_request_class

app = Flask(__name__)
app.debug = True
xml_path = app.config['UPLOADED_FILES_DEST'] = os.path.realpath('./static/timetable/')  # 文件储存地址
FILES = ('xlsx')
timetable = UploadSet('files', FILES)
configure_uploads(app, timetable)
patch_request_class(app)  # 文件大小限制，默认为16MB

#上下文终止
@app.teardown_appcontext
def close_connection(exeption):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
#首页
@app.route("/")
def home_page():
    return render_template('home.html')
#ip地址列表页
@app.route("/url_list/")
def url_table():
    return render_template('url_list.html')
#故障登记页面
@app.route("/feedback/")
def feedback():

    sql = 'select ROWID,CategoryName from category'
    categories = query_sql(sql)
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

        sql = "insert into feedback(Subject,CategoryID,Feedback,Process,Phone,Body,State,Reply,ReleaseTime) values (?,?,?,?,?,?,?,?,?)"
        execute_sql(sql,(subject,categoryid,feedback,process,phone,body,state,reply,releasetime))
        return redirect(url_for('feedback'))
#测试
@app.route('/test/')
def test():
    return 'test'
# 管理员列表编辑页
@app.route('/admin/list/')
def feedback_list():
    key =request.args.get('key', '')
    sql = 'select ROWID,* from feedback WHERE Subject LIKE ? ORDER BY ROWID DESC '
    feedbacks = query_sql(sql, ('%{}%'.format(key),))
    return render_template('feedback_list.html',feedback_list = feedbacks)
# 删除列表
@app.route('/admin/list/del/<id>')
def del_list(id):
    sql = 'delete from feedback WHERE ROWID = ?'
    execute_sql(sql, (id,))
    return redirect(url_for('feedback_list'))
# 编辑列表
@app.route('/admin/list/edit/<id>')
def edit_list(id):
    sql = 'select rowid,CategoryName from category'
    categories = query_sql(sql)
    sql = 'select rowid,* from feedback WHERE ROWID = ?'
    current_feedback = query_sql(sql, (id,), one=True)
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
        execute_sql(sql,(subject,categoryid,feedback,process,phone,body,state,releasetime,rowid))
        return redirect(url_for('feedback_list'))
#查看详细列表
@app.route('/admin/list/search_list/<id>')
def search_list(id):

    sql = 'select rowid,CategoryName from category'
    categories = query_sql(sql)

    sql = 'select rowid,* from feedback WHERE ROWID = ?'
    current_feedback = query_sql(sql, (id,), one=True)

    return render_template('search.html', categories=categories, item=current_feedback)
#表格页面
@app.route('/sheet/<id>')
def sheet(id):
    if id == 'otsheet':
        return render_template('otsheet.html')
    elif id == 'hotsheet':
        return render_template('hotsheet.html')
    elif id == 'annsheet':
        return render_template('annsheet.html')
    elif id =='bsnssheet':
        return render_template('bsnssheet.html')
@app.route('/post_sheet/',methods=['POST'])
def post_sheet():
    sheet = request.form['sheet']
    if sheet == 'otsheet':
        if request.method == 'POST':
            names = request.form['names']
            department = request.form['department']
            position = request.form['position']
            thing = request.form['thing']
            date = request.form['date']
            place = request.form['place']
            ottime = request.form['ottime']
            datetimeStart = request.form['datetimeStart']
            datetimeEnd = request.form['datetimeEnd']
            make_otsheet(names, department, position, thing, date, place, ottime, datetimeStart, datetimeEnd)
            return send_from_directory("./static/sheet", "otsheet.xlsx", as_attachment=True)
    elif sheet == 'hotsheet':
        if request.method == 'POST':
            name1 = request.form['name1']
            name2 = request.form['name2']
            name3 = request.form['name3']
            name4 = request.form['name4']
            name5 = request.form['name5']
            position1 = request.form['position1']
            position2 = request.form['position2']
            position3 = request.form['position3']
            position4 = request.form['position4']
            position5 = request.form['position5']
            datetimeStart1 = request.form['datetimeStart1']
            datetimeStart2 = request.form['datetimeStart2']
            datetimeStart3 = request.form['datetimeStart3']
            datetimeStart4 = request.form['datetimeStart4']
            datetimeStart5 = request.form['datetimeStart5']
            datetimeEnd1 = request.form['datetimeEnd1']
            datetimeEnd2 = request.form['datetimeEnd2']
            datetimeEnd3 = request.form['datetimeEnd3']
            datetimeEnd4 = request.form['datetimeEnd4']
            datetimeEnd5 = request.form['datetimeEnd5']
            thing = request.form['thing']
            make_hotsheet(name1,name2,name3,name4,name5,position1,position2,position3,position4,position5,datetimeStart1,datetimeStart2,datetimeStart3,datetimeStart4,datetimeStart5,datetimeEnd1,datetimeEnd2,datetimeEnd3,datetimeEnd4,datetimeEnd5,thing)
            return send_from_directory("./static/sheet", "hotsheet.xlsx", as_attachment=True)
    elif sheet == 'annsheet':
        if request.method == 'POST':
            names = request.form['names']
            department = request.form['department']
            position = request.form['position']
            thing = request.form['thing']
            datetimeStart = request.form['datetimeStart']
            datetimeEnd = request.form['datetimeEnd']
            thing1 = request.form['thing1']
            make_annsheet(names,department,position,thing,datetimeStart,datetimeEnd,thing1)
            return send_from_directory("./static/sheet","annsheet.xlsx", as_attachment=True)
    elif sheet == 'bsnssheet':
        if request.method == 'POST':
            names = request.form['names']
            department = request.form['department']
            personnel = request.form['personnel']
            datetimeStart = request.form['datetimeStart']
            datetimeEnd = request.form['datetimeEnd']
            thing = request.form['thing']
            thing1 = request.form['thing1']
            inform = request.form['inform']
            outform = request.form['outform']
            announcement = request.form['announcement']
            thing2 = request.form['thing2']
            thing3 = request.form['thing3']
            make_bsnssheet(names,department,personnel,datetimeStart,datetimeEnd,thing,thing1,inform,outform,announcement,thing2,thing3)
            return send_from_directory("./static/sheet","bsnssheet.xlsx", as_attachment=True)
@app.route('/timetable/',methods=['GET', 'POST'])
def timetables():
    if request.method == 'POST' and 'timetable' in request.files:
        timetable.save(request.files['timetable'])
        return redirect('timetable')
    else:
        files_list = os.listdir(xml_path)
        return render_template('timetable.html',files_list=files_list)
@app.route('/timetable_download/<filename>/<type>')
def timetable_download(filename,type):
    if type == 'download':
        return send_from_directory(xml_path,filename)
    elif type == 'del':
        file_path = timetable.path(filename)
        os.remove(file_path)
        return redirect(url_for('timetables'))
@app.route('/monitor/')
def monitor():

    return (render_template('monitor.html'))

if __name__ == "__main__":
    app.run()
