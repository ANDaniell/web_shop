import sqlalchemy
from sqlalchemy import orm
import datetime
from data.db_session import SqlAlchemyBase

GoodToUser = sqlalchemy.Table(
    'good_to_user_table',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users_table', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users_table.id')),
    sqlalchemy.Column('goods_table', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('goods_table.id'))
)


class Good(SqlAlchemyBase):  # , UserMixin, SerializerMixin):
    __tablename__ = 'goods_table'
    # news = orm.relation("News", back_populates='user')
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    avatar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    characteristics = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    discount = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    tags = orm.relation("Tag",
                        secondary="tag_to_good_table",
                        backref="goods_table", )

    # email = sqlalchemy.Column(sqlalchemy.String,index=True, unique=True, nullable=True)

    # TODO связь с rewiew, favourite

    def __repr__(self):
        return f'{self.id} {self.name} {self.about} {self.avatar}'

    def set_avatar(self, path):
        self.avatar = path
