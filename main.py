import os

from flask import Flask, render_template, send_from_directory, url_for, make_response
import datetime

from flask_mail import Mail

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

mail = Mail(app)


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


def main():
    db_session.global_init("db/blogs.db")
    app.run(host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()
