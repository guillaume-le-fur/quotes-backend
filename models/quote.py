import datetime

from db import db
from models.quote_to_tag import quote_to_tags
from models.tag import TagModel
from typing import List

from utils.string_utils import camel_case_keys


class QuoteModel(db.Model):
    __tablename__ = 'Quote'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    book = db.Column(db.String)

    creator = db.relationship(
        "UserModel",
        back_populates="quotes"
    )

    tags = db.relationship(
        'TagModel',
        secondary=quote_to_tags,
        lazy='subquery',
        backref=db.backref('quotes', lazy=True)
    )

    def __init__(
            self,
            creator_id: int,
            creation_date: datetime.datetime,
            text: str,
            author: str = None,
            book: str = None,
            tags: List[str] = None
    ):
        self.creator_id = creator_id
        self.creation_date = creation_date
        self.text = text
        self.author = author
        self.book = book
        self.tags = [TagModel(name=tag) for tag in (tags or [])]

    def json(self):
        return camel_case_keys({
            'id': self.id,
            'creator_id': self.creator_id,
            'creation_date': self.creation_date.isoformat(),
            'text': self.text,
            'author': self.author,
            'book': self.book,
            'tags': [tag.json()["name"] for tag in self.tags]
        })

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
