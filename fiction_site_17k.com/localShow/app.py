from flask import Flask, Response, redirect, url_for, request,render_template,make_response
from utils import (
    search_bookname,
    search_booktype,
    count_booktype,
    get_chapter_list,
    get_chapter,
    valid_login,
    valid_register,
    log,
)
import json


app = Flask(__name__)


@app.route('/')
def index():
    val = request.cookies.get('username',False)
    log('visit:  /  cookies,',request.cookies)
    if not val:
        return  redirect(url_for('login'))
    return render_template("index.html",username=val)


@app.route('/booktype/<string:booktype>/<page>')
def booktype(booktype,page):
    log('visit /booktype/',booktype,page)
    # default int type
    if page == 'about':
        size = str(count_booktype(booktype) )
        # 17k max page is 334 ,max items is 10000,男生,女生types is same ,in max val
        return size
    # when page < 0
    if isinstance(page,str):
        page = int(page)
    rows_list = search_booktype(booktype,int(page))
    return json.dumps(rows_list)


@app.route('/bookname/<string:name>')
def bookname(name):
    log('visit /bookname/', name)
    row =search_bookname(name)
    return json.dumps(row)

@app.route('/book/<bookid>')
def book(bookid):
    return  render_template(
        'chapter.html',
        plus= get_chapter_list(bookid)
    )

# chapter/1503969/22299890.html
@app.route('/chapter/<bookid>/<chapterid>.html')
def chapter(bookid,chapterid):
    # return  'hello world'
    log('visit /chapter',bookid,chapterid,request.query_string)
    h1_text,info,paras = get_chapter(bookid,chapterid, b'vip=True'==request.query_string)

    return render_template(
        'vipReader.html',
        h1_text=h1_text,
        info=info,
        paras=paras
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        log('post: /login ~~~',request.form)
        username = request.form['username']
        password = request.form['password']
        if not valid_login(username,password):
            return render_template('login.html',statusMsg='验证失败,用户名或密码错误')
        r = make_response(redirect(url_for('index')))
        r.set_cookie('username',username)
        return r
    else:
        log('get /login')
        return render_template('login.html')


# somewhere to logout
@app.route("/logout")
def logout():
    keys = [k for k in request.cookies]
    r = make_response(redirect(url_for('login')))
    for k in keys:
        r.delete_cookie(k)
    return r

@app.route('/register',methods=['GET',"POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not valid_register(username,password):
            return render_template(
                'login.html',
                is_login_style=False,
                statusMsg='亲,您已经注册过啦!')
        return render_template(
            'login.html',
            routerPath=url_for('login'),
            statusMsg='注册成功!',
            statusMsgColor='blue'
        )
    else:
        return render_template(
            'login.html',
            is_login_style=False
        )


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


if __name__ == "__main__":
    app.run(
        debug=True,
        # SECRET_KEY='fdsf232',
        port=3000,
    )
