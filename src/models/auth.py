from src.models.base import db


class TokenBlocklist(db.Model):
    __tablename__ = 'token_block_list'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

