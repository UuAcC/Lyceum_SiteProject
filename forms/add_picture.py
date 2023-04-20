from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class PicAddForm(FlaskForm):
    file = FileField('Загрузите файл (ТОЛЬКО в .jpg):', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
