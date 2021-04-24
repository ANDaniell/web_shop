import sqlalchemy
from sqlalchemy import orm
import datetime
from data.db_session import SqlAlchemyBase


class Review(SqlAlchemyBase):  # , UserMixin, SerializerMixin):
    __tablename__ = 'reviews_table'
    # news = orm.relation("News", back_populates='user')
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    grade = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # TODO связь с user and item
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users_table.id"))
    user = orm.relation('User')

    good_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("goods_table.id"))
    good = orm.relation('Good')
