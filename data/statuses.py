import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm
import datetime


class Status(SqlAlchemyBase):
    __tablename__ = 'statuses_table'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    orders = orm.relation("Order", back_populates='status')
