from flask_restful import reqparse

band_parser = reqparse.RequestParser()
band_parser.add_argument('name', required=True)
band_parser.add_argument('genre', required=True)
band_parser.add_argument('created_date', required=True)
band_parser.add_argument('albums', required=True)
band_parser.add_argument('musicians', required=True)

musician_parser = reqparse.RequestParser()
musician_parser.add_argument('name', required=True)
musician_parser.add_argument('surname', required=True)
musician_parser.add_argument('birth_date', required=True)
musician_parser.add_argument('death_date')
musician_parser.add_argument('group', required=True)

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', required=True)
user_parser.add_argument('email', required=True)
user_parser.add_argument('created_date', required=True)
user_parser.add_argument('is_admin')
