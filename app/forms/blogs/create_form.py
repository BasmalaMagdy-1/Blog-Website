from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class CreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=20)])
    content = TextAreaField('content', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Create Blog')
