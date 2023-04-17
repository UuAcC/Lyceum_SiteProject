from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField, FieldList, FormField
from wtforms.validators import DataRequired, Optional


class SongForm(FlaskForm):
    name = StringField('Название песни:', validators=[DataRequired()])
    file = FileField('Аудиозапись (в .mp3):', validators=[Optional()])


class SongsForm(FlaskForm):
    songs = FieldList(FormField(SongForm))
    submit = SubmitField('Подтвердить')
