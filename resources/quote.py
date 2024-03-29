import datetime
import time

import sqlalchemy.exc
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.quote import QuoteModel
from models.tag import TagModel

from models.user import UserModel


def extended_quote_json(quote: QuoteModel):
    q = quote.json()
    q['creatorUsername'] = UserModel.find_by_id(quote.creator_id).username
    return q


class Quote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'text',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'author',
        type=str,
        required=False,
        help="This field can be left blank!"
    )
    parser.add_argument(
        'book',
        type=str,
        required=False,
        help="This field can be left blank!"
    )
    parser.add_argument(
        'tags',
        type=str,
        action='append',
        required=False,
    )
    parser.add_argument(
        'creator_id',
        type=str,
        required=False
    )

    @jwt_required()
    def get(self, _id):
        quote = QuoteModel.find_by_id(_id)
        if quote:
            return extended_quote_json(quote=quote)
        return {'message': 'quote not found'}, 404

    @jwt_required()
    def delete(self, _id):
        quote = QuoteModel.find_by_id(_id)
        if quote:
            quote.delete_from_db()
            return {'message': 'quote deleted.'}, 200
        return {'message': 'quote not found.'}, 404

    @jwt_required()
    def put(self, _id: str = None):
        _id = int(_id)
        data = Quote.parser.parse_args()
        if _id is not None and _id > 0:
            quote = QuoteModel.find_by_id(_id)
            if quote:
                quote.text = data['text']
                quote.author = data["author"]
                quote.book = data["book"]
                quote.tags = [TagModel(tag) for tag in (data.get("tags", []))]
            else:
                return {'message': 'quote not found, provide ID 0 to create quote'}, 404
        else:
            data['creation_date'] = datetime.datetime.now()
            quote = QuoteModel(**data)
        quote.save_to_db()
        return quote.json(), 200


class QuoteList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'text',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'author',
        type=str,
        required=False,
        help="This field can be left blank!"
    )
    parser.add_argument(
        'book',
        type=str,
        required=False,
        help="This field can be left blank!"
    )
    parser.add_argument(
        'tags',
        type=str,
        action='append',
        required=False,
    )
    parser.add_argument(
        'creator_id',
        type=str,
        required=False
    )

    @jwt_required()
    def get(self, filter_text: str = None):
        if filter_text:
            result = QuoteModel.query.filter(QuoteModel.text.ilike(f'%{filter_text}%')).all()
        else:
            result = QuoteModel.query.all()
        return {
            'quotes': list(map(
                extended_quote_json,
                result
            ))
        }

    @jwt_required()
    def post(self):
        data = QuoteList.parser.parse_args()
        quote = QuoteModel(**data)
        try:
            quote.save_to_db()
        except sqlalchemy.exc.SQLAlchemyError:
            return {"message": "An error occurred inserting the quote."}, 500
        return quote.json(), 201

    @jwt_required()
    def delete(self):
        quotes = QuoteModel.query.all()
        if quotes:
            try:
                [quote.delete_from_db() for quote in quotes]
            except sqlalchemy.exc.SQLAlchemyError:
                return {"message": "An error occurred deleting the quotes."}, 500
            return {'message': 'quotes deleted.'}, 200
        return {'message': 'no quotes found.'}, 404
