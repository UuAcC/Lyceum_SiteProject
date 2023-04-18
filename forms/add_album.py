from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AlbumAddForm(FlaskForm):
    name = StringField('Название:', validators=[DataRequired()])
    created_date = StringField('Дата создания:', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class AlbumRedForm(FlaskForm):
    name = StringField('Название:')
    created_date = StringField('Дата создания:')
    submit = SubmitField('Подтвердить')
