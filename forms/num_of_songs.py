from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class NumForm(FlaskForm):
    num = IntegerField('Сколько песен вы хотите разместить?', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
