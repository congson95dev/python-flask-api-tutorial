from src.models.base import db
from sqlalchemy.orm import backref
from datetime import datetime


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    # add foreign key
    # foreign_keys is used because of this table is having 2 columns connect to the same table "users"
    # it throwing an error, so we use foreign_keys to fix it
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = db.relationship("User", backref=backref("books"), foreign_keys=[author_id])
    pages_num = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # add foreign key
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))


