import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm
import datetime

TagToGood = sqlalchemy.Table(
    'tag_to_good_table',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('goods_table', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('goods_table.id')),
    sqlalchemy.Column('tags_table', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tags_table.id'))
)


class Tag(SqlAlchemyBase):
    __tablename__ = 'tags_table'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
