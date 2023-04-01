import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
# from sqlalchemy_serializer import SerializerMixin


class Album(SqlAlchemyBase):
    __tablename__ = 'albums'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    created_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("groups.id"))
