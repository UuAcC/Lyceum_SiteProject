from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FileField
from wtforms.validators import DataRequired


class AlbumAddForm(FlaskForm):
    name = StringField('Название:', validators=[DataRequired()])
    created_date = StringField('Дата создания:', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
