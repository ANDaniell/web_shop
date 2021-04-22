import sqlalchemy
from sqlalchemy import orm
import datetime
from data.db_session import SqlAlchemyBase


class item_image(SqlAlchemyBase):  # , UserMixin, SerializerMixin):
    __tablename__ = 'item_images_table'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("goods_table.id"))
    item = orm.relation('Good')
