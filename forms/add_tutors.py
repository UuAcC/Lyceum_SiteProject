from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FieldList, FormField


class TutForm(FlaskForm):
    name = StringField('Песня:')
    url = StringField('Ссылка:', default='None')


class TutorsForm(FlaskForm):
    songs = FieldList(FormField(TutForm))
    submit = SubmitField('Подтвердить')