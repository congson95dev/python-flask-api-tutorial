from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

from src.models.base import db
from sqlalchemy.orm import backref
from datetime import datetime


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = db.relationship("User", backref=backref("books"), foreign_keys=[author_id])
    pages_num = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)
    rate = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_date = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    deleted_date = db.Column(db.DateTime, nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    @hybrid_property
    def title_author(self):
        if not self.title:
            self.title = ""
        if not self.author_id:
            self.author.username = ""
        return self.title + " - " + self.author.username
