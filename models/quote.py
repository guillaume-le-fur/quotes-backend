from db import db
from models.quote_to_tag import quote_to_tags


class QuoteModel(db.Model):
    __tablename__ = 'Quote'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    author = db.Column(db.String)
    book = db.Column(db.String)

    tags = db.relationship(
        'TagModel',
        secondary=quote_to_tags,
        lazy='subquery',
        backref=db.backref('quotes', lazy=True)
    )

    def __init__(self, text: str, author: str = None, book: str = None):
        self.text = text
        self.author = author
        self.book = book

    def json(self):
        return {
            'id': self.id,
            'text': self.text,
            'author': self.author,
            'book': self.book
        }

    @classmethod
    def find_by_id(cls, _id: int) -> 'QuoteModel':
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name) -> 'QuoteModel':
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
