from db import db

quote_to_tags = db.Table('QuoteToTag',
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'), primary_key=True),
    db.Column('quote_id', db.Integer, db.ForeignKey('Quote.id'), primary_key=True)
)
