from flask_wtf.form import FlaskForm
from wtforms.fields import StringField, TextAreaField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileRequired, FileField


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
        validators=[
            DataRequired(message='本文は必須です。'),
        ]
    )

    category = StringField(
        'カテゴリ',
        validators=[
            DataRequired(message='カテゴリは必須です。'),
            Length(max=50, message='50文字以内で入力してください。'),
        ]
    )

    tag = HiddenField(
        'タグ',
        validators=[]
    )

    is_public = BooleanField(
        '公開',
        validators=[]
    )

    thumbnail_image = FileField(
        validators=[
            FileRequired('画像ファイルを指定してください。'),
            FileAllowed(['png', 'jpg', 'jpeg'], 'サポートされていない画像形式です。'),
        ]
    )

    submit = SubmitField()
