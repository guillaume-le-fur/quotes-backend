import uuid
from datetime import timedelta

from flask import Flask, request, jsonify, make_response
from flask_restful import Api
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp

from models import quote_to_tag
from models.quote import QuoteModel
from models.tag import TagModel
from models.user import UserModel
from populate_db import populate
from resources.quote import Quote, QuoteList
from resources.tag import Tag
from db import db
from resources.user import User

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.drop_all()
    db.create_all()

    # for model in [TagModel, QuoteModel, UserModel, quote_to_tag]:
    #     print(model)
    #     db.session.query(model).delete()
    #     db.session.commit()
    populate()


# def authenticate(username, password):
#     user = UserModel.find_by_username(username=username)
#     if user and safe_str_cmp(
#             user.password.encode('utf-8'),
#             generate_password_hash(password, method='sha256').encode('utf-8')
#     ):
#         return user
#
#
# def identity(payload):
#     user_id = payload['identity']
#     return UserModel.find_by_id(user_id)


jwt = JWTManager(app)

api.add_resource(Quote, '/quote/<string:_id>')
api.add_resource(QuoteList, '/quotes/<string:filter_text>', '/quotes')
api.add_resource(Tag, '/tag')
api.add_resource(User, '/user')


@jwt.user_identity_loader
def user_identity_lookup(user: UserModel):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=identity).one_or_none()


@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = UserModel.query.filter_by(username=auth.username).first()

    if user is None:
        return make_response('user not found', 404, {'WWW.Authentication': 'Basic realm: "login required"'})

    if user.check_password(auth.password):
        token = create_access_token(identity=user).decode("utf-8")
        return jsonify(
            accessToken=token,
            **user.json()
        )

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        data = request.get_json()
        if UserModel.find_by_username(data.get('username')) is not None:
            return jsonify({'message': 'username already exists'}), 409
        hashed_password = generate_password_hash(data.get('password'), method='sha256')
        new_user = UserModel(
            public_id=str(uuid.uuid4()),
            email=data.get('email'),
            username=data.get('username'),
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'registered successfully'}), 201


if __name__ == '__main__':
    print(
        """		__________  ____________________________________
               / ___  /  /  /  /  __   /___  ___/  _____/   ____/
              / /  / /  /  /  /  / /  /   / /  /  /__  /   /___
             / /  / /  /  /  /  / /  /   / /  /  ___/ /____   /
            / /__/ /  /__/  /  /_/  /   / /  /  /____ ____/  /
           /___   /________/_______/   /_/  /_______//______/
               \\__\\
        """

    )
    app.run(port=5000, debug=True)
