from flask_restful import Resource, reqparse
from models.tag import TagModel


class Tag(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, name):
        quote = TagModel.find_by_name(name)
        if quote:
            return quote.json()
        return {'message': 'tag not found'}, 404

    def post(self, name):
        if TagModel.find_by_name(name):
            return {'message': "A tag with name '{}' already exists.".format(name)}, 400

        data = Tag.parser.parse_args()

        quote = TagModel(name)

        try:
            quote.save_to_db()
        except:
            return {"message": "An error occurred inserting the tag."}, 500

        return quote.json(), 201

    def delete(self, name):

        quote = TagModel.find_by_name(name)
        if quote:
            quote.delete_from_db()
            return {'message': 'tag deleted.'}
        return {'message': 'tag not found.'}, 404

    def put(self, name):

        data = Tag.parser.parse_args()

        quote = TagModel.find_by_name(name)

        if quote:
            quote.text = data['text']
        else:
            quote = TagModel(name)

        quote.save_to_db()

        return quote.json()
