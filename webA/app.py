import uuid

from flask import Flask, render_template, make_response, session
from flask import redirect
from flask import request
from flask import url_for

app = Flask(__name__)

app.secret_key = '123'
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # 取到表单中提交上来的参数
        username = request.form.get("username")
        password = request.form.get("password")

        if not all([username, password]):
            return make_response('用户名或密码错误')
        else:
            print(username, password)
            if username == 'halon' and password == '123':
                # 状态保持，设置用户名到cookie中表示登录成功
                response = redirect(url_for('transfer'))
                response.set_cookie('username', username)
                return response
            else:
                return make_response('密码错误')
    else:
        return render_template('login.html')


@app.route('/transfer', methods=["POST", "GET"])
def transfer():
    # 从cookie中取到用户名
    username = request.cookies.get('username', None)
    # 如果没有取到，代表没有登录
    if not username:
        return redirect(url_for('index'))

    if request.method == "POST":
        csrf_token = request.form.get('csrf_token')
        csrf_token_session = session.get('csrf_token')
        if csrf_token == csrf_token_session:

            to_account = request.form.get("to_account")
            money = request.form.get("money")
            print('假装执行转操作，将当前登录用户的钱转账到指定账户')
            return '转账 %s 元到 %s 成功' % (money, to_account)
        else:
            return '小样'
    else:
        # 生成随机码
        csrf_token = str(uuid.uuid1())
        csrf_token = csrf_token.replace('-','')
        session['csrf_token'] = csrf_token
        # 渲染转换页面
        response = make_response(render_template('transfer.html',csrf_token=csrf_token))
        return response


if __name__ == '__main__':
    num = 3
    app.run(port=11000)
