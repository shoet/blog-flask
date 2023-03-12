from flask_wtf.form import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField(
            'メールアドレス',
            validators=[
                DataRequired(message='メールアドレスは必須です。'),
                Email(message='メールアドレスの形式で入力してください。'),
                ]
            )

    password = PasswordField(
            'パスワード',
            validators=[
                DataRequired(message='パスワードは必須です。'),
                ]
            )

    submit = SubmitField('ログイン')
