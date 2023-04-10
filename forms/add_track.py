from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class MusAddForm(FlaskForm):
    def __init__(self, songs):
        super().__init__()
        self.songs = [{f'{song.name}': FileField(f'Загрузите файл для {song.name}:')} for song in songs]
    submit = SubmitField('Подтвердить')