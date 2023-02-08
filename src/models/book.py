from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

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
    rate = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_date = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    deleted_date = db.Column(db.DateTime, nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    # @hybrid_property is used to set a new field which doesn't save in db
    # in this example, i've created a new field "title_author" which doesn't exists in db
    # Ex: title_author = title + " - " + author.username
    # This feature used to set "fullname" for table "user", in case table "user" only have "firstname" and "lastname"
    # Ex: fullname = firstname + " - " + lastname
    @hybrid_property
    def title_author(self):
        if not self.title:
            self.title = ""
        if not self.author_id:
            self.author.username = ""
        return self.title + " - " + self.author.username



