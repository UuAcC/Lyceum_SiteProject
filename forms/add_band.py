from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class BandAddForm(FlaskForm):
    name = StringField('Название группы:', validators=[DataRequired()])
    genre = StringField('Жанр:', validators=[DataRequired()])
    created_date = StringField('Дата создания:', validators=[DataRequired()])
    closed_date = StringField('Дата распада:', default='живы ещё')
    short_bio = TextAreaField('Краткая биография:', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class BandRedForm(FlaskForm):
    name = StringField('Название группы:')
    genre = StringField('Жанр:')
    created_date = StringField('Дата создания:')
    closed_date = StringField('Дата распада:')
    short_bio = TextAreaField('Краткая биография:')
    submit = SubmitField('Подтвердить')
