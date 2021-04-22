import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users_table'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    hashed_address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_card = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # TODO связь с rewiew, favourite

    orders = orm.relation("Order", back_populates='user')

    favourites = orm.relation("Good",
                              secondary="good_to_user_table",
                              backref="users_table", )
