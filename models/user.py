from werkzeug.security import check_password_hash

from db import db


class UserModel(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    quotes = db.relationship(
        'QuoteModel',
        back_populates='creator'
    )

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'is_admin': self.is_admin
        }

    @classmethod
    def find_by_id(cls, _id: int) -> 'UserModel':
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username) -> 'UserModel':
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)
