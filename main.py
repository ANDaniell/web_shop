import os

from flask import Flask, render_template, send_from_directory, url_for, make_response
import datetime
from data import db_session
from data.goods import Good
from data.item_images import item_image
from data.location import Address
from data.orders import Order
from data.reviews import Review
from data.statuses import Status
from data.tags import Tag, TagToGood
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jbbsdckcbsddcbhulchb27e26gdc76wg7'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)


@app.route('/')
def index():
    return make_response(render_template('index.html'))


@app.route('/items/')
def items():
    return make_response(render_template('items.html'))


@app.route('/items/item/<id_item>')
def item(id_item):
    return make_response(render_template('item.html'))


@app.route('/img/<path:path>')
def img(path):
    return send_from_directory('static', path)


@app.route('/test')
def test():
    url = url_for('item', id_item='101')
    return make_response(render_template('test.html', item1=url))


def clear_data():
    os.remove("db/blogs.db")


def add_item(name, price, pth_to_img_avatar, about, char, amount, tags=None, discount=None):
    db_sess = db_session.create_session()
    item = Good(
        name=str(name),
        price=float(price),
        avatar=str(pth_to_img_avatar),
        about=str(about),
        characteristics=str(char),
        amount=int(amount),
        # tags=db_sess.query(Tag).filter(Tag.id == 1).all()
    )
    if tags:
        item.tags = db_sess.query(Tag).filter(eval(tags)).all()
    if discount:
        item.discount = float(discount)

    db_sess.add(item)
    db_sess.commit()


def add_item_image(path_to_img, item_id):
    db_sess = db_session.create_session()
    item_img = item_image(
        path=str(path_to_img),
        item_id=int(item_id)
    )
    db_sess.add(item_img)
    db_sess.commit()


def add_tag_to_item(item_id, tag_id):
    db_sess = db_session.create_session()
    item = db_sess.query(Good).filter(Good.id == item_id).first()
    tag = db_sess.query(Tag).filter(Tag.id == tag_id).first()
    item.tags.append(tag)
    db_sess.commit()


def add_tag(name):
    db_sess = db_session.create_session()
    tag = Tag(
        name=str(name)
    )
    db_sess.add(tag)
    db_sess.commit()


def add_order(item_id, user_id, address_id, price=0, status_id=1):
    db_sess = db_session.create_session()
    order = Order(
        total_price=float(price),
        status_id=int(status_id),
        goods_by_order = db_sess.query(Good).filter(Good.id == 2).all()
    )
    # order.goods = db_sess.query(Good).filter(Good.id == 2).all()
    order_id = order.id
    if user_id:
        order.user_id = int(user_id)
    if address_id:
        order.address_id = int(address_id)
    db_sess.add(order)
    db_sess.commit()
    add_item_to_order(item_id, order_id)


def add_item_to_order(item_id, order_id):
    db_sess = db_session.create_session()
    item = db_sess.query(Good).filter(Good.id == item_id).first()
    order = db_sess.query(Order).filter(Order.id == order_id).first()
    order.goods.append(item)
    db_sess.commit()


def add_status(name):
    db_sess = db_session.create_session()
    status = Status(
        name=str(name)
    )
    db_sess.add(status)
    db_sess.commit()


def add_user(name, email, password, address_id=None, card=None):
    db_sess = db_session.create_session()
    user = User(
        name=str(name),
        email=str(email),
        hashed_password=str(password),
        hashed_card=str(card)
    )
    if address_id:
        user.address_id = int(address_id)
    if card:
        user.hashed_card = int(card)
    db_sess.add(user)
    db_sess.commit()


def add_favourite(item_id, user_id):
    db_sess = db_session.create_session()
    item = db_sess.query(Good).filter(Good.id == int(item_id)).first()
    user = db_sess.query(User).filter(User.id == int(user_id)).first()
    user.favourites.append(item)
    db_sess.commit()


def add_review(grade, item_id, user_id=None, about=None):
    db_sess = db_session.create_session()
    rewiew = Review(
        grade=int(grade),

        good_id=int(item_id)
    )
    if about:
        rewiew.about = str(about)
    if user_id:
        rewiew.user_id = int(user_id)
    db_sess.add(rewiew)
    db_sess.commit()


def add_address(city, region):
    db_sess = db_session.create_session()
    address = Address(
        city=str(city),
        region=str(region)
    )
    db_sess.add(address)
    db_sess.commit()


def main():
    db_session.global_init("db/blogs.db")
    '''
    
    # 
    
    
    

    add_item_to_order(2, 1)
    add_favourite(1, 1)
    add_review(4, 1, 1, 'сообщение от user1')
    '''

    # add_user('Evgen', 'evgen@gmail.com', 'password', None, None)
    # add_address('Moscow', "Moscow region")
    # add_user('Evgen2', 'evgen2@gmail.com', 'password', None, None)
    # add_tag('tag 01')
    # add_tag('tag 02')
    # add_item('item_name', 3000, 'path_toImg', 'about', 'харктеристики', 3, 'Tag.id == 1')
    # add_item('item_name2', 3001, 'path_toImg', 'about', 'харктеристики', 3)

    # add_tag_to_item(1, 2)
    # add_item_image('путь до картинки', 1)
    # add_status('status 1')
    add_order(1, 1, 1, 300, 1)

    # app.register_blueprint(news_api.blueprint)

    # app.run(debug=True)


if __name__ == '__main__':
    main()
    # with app.test_request_context():
    # print(url_for('item'))
    # app.run(host='127.0.0.1', debug=True)
