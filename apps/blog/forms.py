from flask_wtf.form import FlaskForm
from wtforms.fields import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField(
            'タイトル',
            validators=[
                DataRequired(message='タイトルは必須です。'),
                Length(max=50, message='50文字以内で入力してください。'),
                ]
            )

    body = TextAreaField(
            '本文',
            validators=[]
            )

    is_public = BooleanField(
            '公開',
            validators=[]
            )

    submit = SubmitField()
