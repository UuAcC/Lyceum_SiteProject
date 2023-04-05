from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired


class PicAddForm(FlaskForm):
    file = FileField('Загрузите файл:', validators=[DataRequired()])
    band = BooleanField('Для группы')
    album = BooleanField('Для альбома')
    musician = BooleanField('Для музыканта')
    submit = SubmitField('Подтвердить')
