import os

from flask import Flask, render_template, send_from_directory, url_for, make_response
import datetime
from data import db_session
from data.goods import Good
from data.item_images import item_image
from data.orders import Order
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


def add_item():
    db_sess = db_session.create_session()
    item = Good(
        name='phone',
        price='300',
        avatar='something',
        about="simple",
        characteristics='крутой',
        discount=0,
        amount=3,
        tags=db_sess.query(Tag).filter(Tag.id == 1).all()
    )
    db_sess.add(item)
    db_sess.commit()


def add_item_image():
    db_sess = db_session.create_session()
    item_img = item_image(
        path='path to image',
        item_id=1
    )
    db_sess.add(item_img)
    db_sess.commit()


def add_tag_to_item():
    db_sess = db_session.create_session()
    item = db_sess.query(Good).filter(Good.id == 1).first()
    tag = db_sess.query(Tag).filter(Tag.id == 2).first()
    item.tags.append(tag)
    db_sess.commit()


def add_tag():
    db_sess = db_session.create_session()
    tag = Tag(
        id=1,
        name='tag name'
    )
    db_sess.add(tag)
    tag = Tag(
        id=2,
        name='tag name 02'
    )
    db_sess.add(tag)
    db_sess.commit()


def add_order():
    db_sess = db_session.create_session()
    tag = Order(
        id=1,
        total_price=12121,
        status_id=1
    )
    db_sess.add(tag)
    db_sess.commit()


def add_status():
    db_sess = db_session.create_session()
    status = Status(
        id=1,
        name='name'
    )
    db_sess.add(status)
    db_sess.commit()


def add_user():
    db_sess = db_session.create_session()
    status = User(
        name='Mike',
        email="mike@gmail.com",
        hashed_password='a'
    )
    db_sess.add(status)
    db_sess.commit()


def main():
    db_session.global_init("db/blogs.db")
    add_tag()
    add_item()
    add_item_image()
    add_tag_to_item()
    # add_status()
    # add_order()

    # app.register_blueprint(news_api.blueprint)

    # app.run(debug=True)


if __name__ == '__main__':
    main()
    # with app.test_request_context():
    # print(url_for('item'))
    # app.run(host='127.0.0.1', debug=True)
