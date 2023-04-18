from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from data import db_session
from data.groups import Group

db_session.global_init("db/music.db")
db_sess = db_session.create_session()


class MusicianAddForm(FlaskForm):
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    birth_date = StringField('Дата рождения:', validators=[DataRequired()])
    death_date = StringField('Дата смерти:')
    group_id = RadioField('Выберите группу, в которой играл музыкант:   ', validators=[DataRequired()],
                          choices=[(band.id, band.name) for band in db_sess.query(Group).all()])
    short_bio = TextAreaField('Краткая биография:', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class MusicianRedForm(FlaskForm):
    name = StringField('Имя:')
    surname = StringField('Фамилия:')
    birth_date = StringField('Дата рождения:')
    death_date = StringField('Дата смерти:')
    group_id = RadioField('Выберите группу, в которой играл музыкант:   ', validators=[DataRequired()],
                          choices=[(band.id, band.name) for band in db_sess.query(Group).all()])
    short_bio = TextAreaField('Краткая биография:')
    submit = SubmitField('Подтвердить')
