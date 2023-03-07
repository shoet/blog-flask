from datetime import datetime

from apps.app import db


class PostItem(db.Model):
    __tablename__ = 'post_item'
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    post_tags = db.relationship('PostTag', backref='post_item')


class PostTag(db.Model):
    __tablename__ = 'post_tag'
    id = db.Column(db.String, primary_key=True)
    post_id = db.Column(db.String, db.ForeignKey('post_item.id'))
    tag_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
