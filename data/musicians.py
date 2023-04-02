import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Musician(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'musicians'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    birth_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    death_date = sqlalchemy.Column(sqlalchemy.String)
    group_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("groups.id"))
    short_bio = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
