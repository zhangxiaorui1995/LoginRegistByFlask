# -*- conding=UTF-8 -*-
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)

app.config.from_object(config)
db = SQLAlchemy(app)


# 对flask进行一个初始化
# 创建一个simple表
class Simple(db.Model):
    __tablename__ = 'simple'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(100), nullable=False, unique=True)
    pwd = db.Column(db.CHAR(50), nullable=False, unique=True)


db.create_all()


@app.route('/')
# -----------------------------------------------------------
def index():
    return redirect(url_for("login_html"))
    # return "这是一个首页"


@app.route('/lsuccess/', methods=['post', 'GET'])
def login():
    if request.method == "POST":
        user = request.form.get('username')
        pwd = request.form.get('password')

        user_ = Simple.query.filter(Simple.user == user).first()
        if user == Simple.user and pwd == Simple.pwd:
            print("参数请求不正常")
            print(type(Simple.user))
            print(Simple.user)
            return "存在异常，参数请求错误"
        elif user_.user != user:
            print("用户不存在！")
            return redirect(url_for("login_html"))
        elif user_.user == user:
            if user_.pwd == pwd:
                return redirect(url_for('static', filename='index.html'))
            else:
                print("密码错误！")
                return redirect(url_for("login_html"))
        else:
            # result = Simple.query.filter(Simple.user == user and Simple.pwd == pwd).first()
            # return (" username = %s  pwd = %s" %(result.user ,result.pwd))
            # return ("username = %s pwd = %s") %(user, pwd)
            return "你这是什么操作"
    if request.method != 'get':
        return "前端的锅"


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         user = User(
#             username=form.username.data,
#             password=form.password.data
#         )
#         if(User.query.filter_by(username=user.username).first()):
#             flash("当前用户名已经注册！")
#             return render_template("/register.html", form=form)
#         else:
#             flash("注册成功!")
#             db.session.merge(user)
#             return render_template("/register.html", form=form)
#     return render_template("/register.html", form=form)

@app.route('/rsuccess/', methods=['POST', 'GET'])
def regist_function():
    if request.method == "POST":
        user = request.form.get('rename')
        user_ = Simple.query.filter(Simple.user == user).first()
        if user == user_.user:
            print("此用户已存在")
            return redirect(url_for("regist_html"))
        else:
            password = request.form.get('repwd')
            simple1 = Simple(user=user, pwd=password)
            db.session.add(simple1)
            db.session.commit()
            # return "注册成功  账号 = %s  密码= %s" % (user, password)
            # pass
            return redirect(url_for("login_html"))


@app.route('/regist/')
def regist_html():
    return render_template('regist.html')


@app.route('/login/')
def login_html():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
