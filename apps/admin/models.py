from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from apps.app import db, login_manager


class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now)

    post_tags = db.relationship('PostItem', backref='admin_user')

    @property
    def password(self):
        raise NotImplementedError

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_duplicate_email(self):
        return AdminUser.query.filter_by(email=self.email).first() is not None

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(user_id)