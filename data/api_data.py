from flask import jsonify
from flask_restful import Resource, abort
from data import db_session
from data.groups import Group
from data.musicians import Musician
from data.parser import band_parser, musician_parser, user_parser
from data.users import User


def abort_if_not_found(clas, id):
    session = db_session.create_session()
    news = session.query(clas).get(id)
    if not news:
        abort(404, message=f"Item {id} not found")


class BandsResource(Resource):
    def get(self, bands_id):
        abort_if_not_found(Group, bands_id)
        session = db_session.create_session()
        band = session.query(Group).get(bands_id)
        return jsonify({'band': {'name': band.name, 'genre': band.genre, 'created_date': band.created_date,
                                 'albums': [alb.name for alb in band.albums],
                                 'musicians': [(mus.name, mus.surname) for mus in band.musicians]}})

    def delete(self, bands_id):
        abort_if_not_found(Group, bands_id)
        session = db_session.create_session()
        band = session.query(Group).get(bands_id)
        session.delete(band)
        session.commit()
        return jsonify({'success': 'OK'})


class BandsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        band = session.query(Group).all()
        return jsonify({'bands': [{'name': item.name, 'genre': item.genre, 'created_date': item.created_date,
                                   'albums': [alb.name for alb in item.albums],
                                   'musicians': [' '.join([mus.name, mus.surname]) for mus in item.musicians]} for item
                                  in band]})

    def post(self):
        args = band_parser.parse_args()
        session = db_session.create_session()
        band = Group(
            name=args['name'],
            genre=args['genre'],
            created_date=args['created_date'],
        )
        session.add(band)
        session.commit()
        return jsonify({'success': 'OK'})


class MusiciansResource(Resource):
    def get(self, mus_id):
        abort_if_not_found(Musician, mus_id)
        session = db_session.create_session()
        mus = session.query(Musician).get(mus_id)
        return jsonify({'musician': {'name': mus.name, 'surname': mus.surname, 'birth_date': mus.birth_date,
                                     'death_date': mus.death_date, 'group': mus.group}})

    def delete(self, mus_id):
        abort_if_not_found(Musician, mus_id)
        session = db_session.create_session()
        mus = session.query(Musician).get(mus_id)
        session.delete(mus)
        session.commit()
        return jsonify({'success': 'OK'})


class MusiciansListResource(Resource):
    def get(self):
        session = db_session.create_session()
        mus = session.query(Musician).all()
        return jsonify({'musicians': [{'name': item.name, 'surname': item.surname, 'birth_date': item.birth_date,
                                      'death_date': item.death_date, 'group': item.group} for item in mus]})

    def post(self):
        args = musician_parser.parse_args()
        session = db_session.create_session()
        mus = Musician(
            name=args['name'],
            surname=args['surname'],
            birth_date=args['birth_date'],
            death_date=args['death_date'],
            group_id=args['group_id']
        )
        session.add(mus)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_not_found(User, user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('name', 'email', 'created_date', 'is_admin'))})

    def delete(self, user_id):
        abort_if_not_found(User, user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('name', 'email', 'created_date', 'is_admin')) for item in user]})

    def post(self):
        args = user_parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            email=args['email'],
            created_date=args['created_date'],
            is_admin=args['is_admin']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
