import string
import datetime
import sqlalchemy
from random import choices
from .db_session import SqlAlchemyBase, create_session


class Files(SqlAlchemyBase):
    __tablename__ = 'files'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    link = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

