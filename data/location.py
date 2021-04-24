import sqlalchemy
from sqlalchemy import orm
import datetime
from data.db_session import SqlAlchemyBase


class Address(SqlAlchemyBase):  # , UserMixin, SerializerMixin):
    __tablename__ = 'address_table'
    # news = orm.relation("News", back_populates='user')
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    region = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String)
    orders = orm.relation("Order", back_populates='address')
    users = orm.relation("User", back_populates='address')