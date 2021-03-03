from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.quote import QuoteModel, quote_to_tags


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

    def put(self, _id):

        data = Quote.parser.parse_args()

        quote = QuoteModel.find_by_id(_id)
        # print(data)
        # print(quote)
        if quote:
            quote.text = data['text']
            quote.author = data["author"]
            quote.book = data["book"]
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

    def get(self):
        return {'quotes': list(map(lambda x: x.json(), QuoteModel.query.all()))}

    def post(self):
        data = QuoteList.parser.parse_args()
        quote = QuoteModel(**data)

        try:
            quote.save_to_db()
        except:
            return {"message": "An error occurred inserting the quote."}, 500

        return quote.json(), 201

    def delete(self):
        quotes = QuoteModel.query.all()
        if quotes:
            try:
                [quote.delete_from_db() for quote in quotes]
            except:
                return {"message": "An error occurred deleting the quotes."}, 500

            return {'message': 'quotes deleted.'}, 200
        return {'message': 'no quotes found.'}, 404
