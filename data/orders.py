import sqlalchemy
from sqlalchemy import orm
import datetime
from data.db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):  # , UserMixin, SerializerMixin):
    __tablename__ = 'orders_table'
    # news = orm.relation("News", back_populates='user')
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    total_price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now)
    status_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("statuses_table.id"))
    status = orm.relation('Status')

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users_table.id"))
    user = orm.relation('User')  #

    address_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("address_table.id"))
    address = orm.relation('Address')

    goods_by_order = orm.relation("Good",
                         secondary="good_to_order_table",
                         backref="orders_table")
