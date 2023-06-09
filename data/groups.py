import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Group(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'groups'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    closed_date = sqlalchemy.Column(sqlalchemy.String, default='живы ещё')
    short_bio = sqlalchemy.Column(sqlalchemy.Text)
    albums = orm.relationship("Album", back_populates='group')
    musicians = orm.relationship("Musician", back_populates="group")
