from flask_restful import Resource, reqparse

from models.user import UserModel


class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, _id):
        user = UserModel.find_by_id(_id)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404
