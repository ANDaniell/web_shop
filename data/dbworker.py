# -*- coding: utf-8 -*-
from werkzeug.security import check_password_hash

from data import db_session
from data.goods import Good
from data.item_images import item_image
from data.location import Address
from data.orders import Order
from data.reviews import Review
from data.statuses import Status
from data.tags import Tag, TagToGood
from data.users import User


class DBWorker():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBWorker, cls).__new__(cls)
            db_session.global_init("db/blogs.db")
            cls.db_sess = db_session.create_session()
        return cls._instance

    def get_db_sess(self):
        return self.db_sess

    def add_user(self, name, email, password, address=None):
        user = User(
            name=str(name),
            email=str(email)
        )
        print(password)
        user.set_hashed_password(password)
        print(user.hashed_password)
        if address:
            if isinstance(address, Address):
                user.address.append(address)
            elif address is int:
                user.address_id = int(address)
        print(name, email, password, address)
        self.db_sess.add(user)
        self.db_sess.commit()
        return user

    def check_user(self, mail, password):
        user = self.db_sess.query(User).filter(User.email == mail).first()
        return check_password_hash(user.hashed_password, password)

    def get_user(self, email):
        user = self.db_sess.query(User).filter(User.email == email).first()
        return user, user.id

    def set_user_data(self, user, **params):
        if user is int:
            user = self.db_sess.query(User).filter(User.id == user).first()
            if user is None:
                raise ValueError(f'No such user with ID {user} in database')
        try:
            for key in params:
                setattr(user, key, params[key])
        except BaseException as be:
            raise ValueError(
                f'Wrong parameters for User class were passed: {be}')
        self.db_sess.update(user)
        self.db_sess.commit()
        return user

    def delete_user(self, user):
        if user is int:
            user = self.db_sess.query(User).filter(User.id == user).first()
            if user is None:
                raise ValueError(f'No such user with ID {user} in database')
        self.db_sess.delete(user)
        self.db_sess.commit()
        return user

    def add_order(self, total_price, status, user=None, address=None, *goods):
        if goods is None or len(goods) == 0:
            raise ValueError(f"Can`t create Order with 0 goods in it: {goods}")
        if user is int:
            user = self.db_sess.query(User).filter(User.id == user).first()
        if address is int:
            address = self.db_sess.query(Address).filter(
                Address.id == address).first()
        order = Order(
            total_price=float(total_price)
        )

        if status is int:
            order.status_id = status
        elif isinstance(status, Status):
            order.status = status

        if user:
            order.user = user
        if address:
            order.address = address

        order.goods_by_order = goods

        self.db_sess.delete(order)
        self.db_sess.commit()
        return order

    def add_good_to_order(self, order, good):
        if order is int:
            order = self.db_sess.query(Order).filter(Order.id == order).first()
            if order is None or len(order) == 0:
                raise ValueError(f'Not found such order')
        if good is int:
            good = self.db_sess.query(Good).filter(Good.id == good).first()
            if good is None:
                raise ValueError(f'Not found such good')

        order.goods_by_order.append(good)
        self.db_sess.update(order)
        self.db_sess.commit()
        return order

    def set_order_data(self, order, **params):
        if order is int:
            order = self.db_sess.query(Order).filter(Order.id == order).first()
            if order is None:
                raise ValueError(f'No such order with ID {order} in database')
        try:
            for key in params:
                setattr(order, key, params[key])
        except BaseException as be:
            raise ValueError(
                f'Wrong parameters for Order class were passed: {be}')
        self.db_sess.update(order)
        self.db_sess.commit()
        return order

    def delete_order(self, order):
        if order is int:
            order = self.db_sess.query(Order).filter(Order.id == order).first()
            if order is None:
                raise ValueError(f'No such order with ID {order} in database')
        self.db_sess.delete(order)
        self.db_sess.commit()
        return order

    def add_good(self, name, price, avatar=None, about=None, characteristics=None, discount=None, amount=None, tags=[]):
        good = Good(
            name=name,
            price=price
        )
        if all([t is int for t in tags]):
            for tag_id in tags:
                tag = self.db_sess.query(Tag).filter(Tag.id == tag_id).first()
                if tag:
                    good.tags.append(tag)
        elif all([isinstance(t, Tag) for t in tags]):
            good.tags = tags
        else:
            raise ValueError(
                f'All tags must be tag_id or Tags instance: {tags}')

        if avatar:
            good.avatar = avatar
        if about:
            good.about = about
        if characteristics:
            good.characteristics = characteristics
        if discount:
            good.discount = discount
        if amount:
            good.amount = amount

        self.db_sess.add(good)
        self.db_sess.commit()
        return good

    def set_good_data(self, good, **params):
        if good is int:
            good = self.db_sess.query(Good).filter(Good.id == good).first()
            if good is None:
                raise ValueError(f'No such good with ID {good} in database')
        try:
            for key in params:
                setattr(good, key, params[key])
        except BaseException as be:
            raise ValueError(
                f'Wrong parameters for Good class were passed: {be}')
        self.db_sess.update(good)
        self.db_sess.commit()
        return good

    def get_goods(self, begin, end):
        arr = []
        for i in range(begin, end):
            good = self.db_sess.query(Good).filter(Good.id == i).first()
            arr.append(
                {'id': good.id, 'name': good.name, 'about': good.about, 'discount': good.discount, 'tags': good.tags,
                 'price': good.price, 'avatar': good.avatar})
        return arr

    def get_good_rating(self, good) -> float:
        if good is int:
            good = self.db_sess.query(Good).filter(Good.id == good).first()
            if good is None:
                raise ValueError(f'No such good with ID {good} in database')

        summ = 0
        for rev in good.review:
            summ += rev.grade

        return summ / len(good.review)

    def search_good(self, query):
        return query

    def count_goods(self):
        rows = self.db_sess.query(Good).count()
        return rows
