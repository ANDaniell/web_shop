import os

from flask import Flask, render_template, send_from_directory, url_for, make_response, request, session
import datetime

from flask_login import login_manager, LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from data import db_session
from data import basket
from data.dbworker import DBWorker
from data.goods import Good
from data.item_images import item_image
from data.location import Address
from data.orders import Order
from data.reviews import Review
from data.statuses import Status
from data.tags import Tag, TagToGood
from data.users import User
from config import ADMINS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jbbsdckcbsddcbhulchb27e26gdc76wg7'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return make_response(render_template('index.html'))


@app.route('/user')
def user():
    dbworker = DBWorker()
    if current_user.is_authenticated:
        print('ok')
        print(current_user.get_id())
        data = dbworker.get_orders(current_user.get_id())
        print(data)
        # user = current_user.get_id()  # return username in get_id()
    else:
        return 'войдите или зарегистрируйтесь'
    return make_response(render_template('user_page.html', user=user, data=data))


@app.route('/items/<number>', methods=['POST', 'GET'])
def items(number):
    dbworker = DBWorker()
    numb = str(number)
    if not numb.isdigit():
        number = 0
    if dbworker.count_goods() > int(number) + 8:
        maxx = (int(number)) * 8 + 1
    else:
        maxx = dbworker.count_goods()
    minn = (int(number) - 1) * 8 + 1
    goods = dbworker.get_goods(minn, maxx)
    leng = maxx - int(number)
    if leng > 4:
        goods_resp = [[goods[0], goods[1], goods[2], goods[3]]]
        gg = []
        for g in goods[4:]:
            gg.append(g)
        leng = len(gg)
        goods_resp.append(gg)
    else:
        goods_resp = [goods]
        leng = len(goods)
    # print(leng)
    flag = (dbworker.count_goods() > (int(number) * 8 + 1))
    res = str(session.get("current_cart"))
    print(session.items(), res)
    if request.method == 'GET':
        return make_response(render_template('items.html',
                                             goods_resp=goods_resp,
                                             number=int(number),
                                             leng=leng, flag=flag))


@app.route('/items/item/<id_item>', methods=['POST', 'GET'])
def item(id_item):
    data = [1, 2, 3, 4]
    dbworker = DBWorker()
    temp = dbworker.get_good(id_item)
    inf = temp['characteristics']
    data = temp['img']
    ab = temp["about"]
    return make_response(render_template('item.html', data=data, inf=inf, about=ab))


@app.route('/img/<path:path>')
def img(path):
    return send_from_directory('static', path)


@app.route('/test')
def test():
    url = url_for('item', id_item='101')
    dbworker = DBWorker()
    dbworker.add_user('Daniel', 'email02@gmail.com', 'password')
    return make_response(render_template('test.html', item1=url))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    dbworker = DBWorker()
    if request.method == 'GET':
        return make_response(render_template('login_user.html'))
    elif request.method == 'POST':
        mail = request.form.get('email')
        passw = request.form.get('password')
        acc = request.form.get('accept')
        print(acc)
        if not dbworker.check_user(mail, passw):
            return make_response(render_template('login_user.html', resp='Ошибка во введённых данных'))

        print(request.form.get('email'))
        print(request.form.get('password'))
        user, user_id = dbworker.get_user(mail)
        login_user(user, remember=acc)
        return redirect('/')


@app.route('/register', methods=['POST', 'GET'])
def UserLogIn():
    if request.method == 'GET':
        return make_response(render_template('user_check_page.html'))
    elif request.method == 'POST':
        name = request.form.get("name")
        mail = request.form.get('email')
        passw = request.form.get('password')
        loc = request.form.get('city_user')

        print(request.form.get("name"))
        print(request.form.get('email'))
        print(request.form.get('password'))
        print(request.form.get('city_user'))
        print(request.form.get('accept'))

        dbworker = DBWorker()
        try:
            dbworker.add_user(name, mail, passw)
            return redirect('/')

        except Exception as e:
            print(e)
            return "Invalid data"


@login_manager.user_loader
def load_user(user_id):
    try:
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)
    except Exception as e:
        print(e)


def send_email(subject, text_body, html_body, sender=ADMINS[0], recipients=ADMINS):
    global ADMINS
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def main():
    mail = Mail(app)
    app.register_blueprint(basket.blueprint)
    app.run(host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()
