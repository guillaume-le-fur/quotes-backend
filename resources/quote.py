import sqlalchemy.exc
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.quote import QuoteModel
from models.tag import TagModel


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

    # @jwt_required()
    def get(self, _id):
        quote = QuoteModel.find_by_id(_id)
        if quote:
            return quote.json()
        return {'message': 'quote not found'}, 404

    def delete(self, _id):
        quote = QuoteModel.find_by_id(_id)
        if quote:
            quote.delete_from_db()
            return {'message': 'quote deleted.'}, 200
        return {'message': 'quote not found.'}, 404

    def put(self, _id: str = None):
        _id = int(_id)
        print("Starting put")
        data = Quote.parser.parse_args()
        print(data)
        if _id is not None and _id > 0:
            quote = QuoteModel.find_by_id(_id)
            print(quote)
            if quote:
                quote.text = data['text']
                quote.author = data["author"]
                quote.book = data["book"]
                quote.tags = [TagModel(tag) for tag in data["tags"]]  # not the best
            else:
                quote = QuoteModel(**data)
        else:
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

    def get(self, filter_text: str = None):
        print(filter_text)
        if filter_text:
            result = QuoteModel.query.filter(QuoteModel.text.ilike(f'%{filter_text}%')).all()
        else:
            result = QuoteModel.query.all()
        return {
            'quotes': list(map(
                lambda x: x.json(),
                result
            ))
        }

    def post(self):
        data = QuoteList.parser.parse_args()
        quote = QuoteModel(**data)
        print(data)
        try:
            quote.save_to_db()
        # TODO specify error.
        except sqlalchemy.exc.SQLAlchemyError:
            return {"message": "An error occurred inserting the quote."}, 500

        return quote.json(), 201

    def delete(self):
        quotes = QuoteModel.query.all()
        if quotes:
            try:
                [quote.delete_from_db() for quote in quotes]
            except sqlalchemy.exc.SQLAlchemyError:
                return {"message": "An error occurred deleting the quotes."}, 500

            return {'message': 'quotes deleted.'}, 200
        return {'message': 'no quotes found.'}, 404
