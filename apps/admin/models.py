from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from apps.app import db


class AdminUser(db.Model):
    __tablename__ = 'admin_user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now)

    @property
    def password(self):
        raise NotImplementedError

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)