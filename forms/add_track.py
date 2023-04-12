from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from data import db_session


class MusAddForm(FlaskForm):
    def __init__(self, res, **kwargs):
        super().__init__(**kwargs)
        self.songs = [{f'{song.name}': FileField(f'Загрузите файл для {song.name}:')} for song in res]
    submit = SubmitField('Подтвердить')