from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.quote import QuoteModel


class Quote(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('text',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # @jwt_required()
    def get(self, name):
        quote = QuoteModel.find_by_name(name)
        if quote:
            return quote.json()
        return {'message': 'quote not found'}, 404

    def post(self, name):
        if QuoteModel.find_by_name(name):
            return {'message': "A quote with name '{}' already exists.".format(name)}, 400

        data = Quote.parser.parse_args()

        quote = QuoteModel(name, **data)

        try:
            quote.save_to_db()
        except:
            return {"message": "An error occurred inserting the quote."}, 500

        return quote.json(), 201

    def delete(self, name):
        quote = QuoteModel.find_by_name(name)
        if quote:
            quote.delete_from_db()
            return {'message': 'quote deleted.'}
        return {'message': 'quote not found.'}, 404

    def put(self, name):
        data = Quote.parser.parse_args()

        quote = QuoteModel.find_by_name(name)

        if quote:
            quote.text = data['text']
        else:
            quote = QuoteModel(name, **data)

        quote.save_to_db()

        return quote.json()


class QuoteList(Resource):
    def get(self):
        return {'quotes': list(map(lambda x: x.json(), QuoteModel.query.all()))}
