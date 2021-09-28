import uuid
import unittest

from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from app import db, app
from models.user import UserModel


class TestUser(TestCase):

    def create_app(self):
        self.app = app.test_client()
        return app

    SQLALCHEMY_DATABASE_URI = "sqlite://"

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'

        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def add_dummy_user(self):
        user = UserModel(
            username='Dummy',
            public_id=str(uuid.uuid4()),
            email='dummy@dummy.com',
            password=generate_password_hash('passwd', method='sha256')
        )
        db.session.add(user)
        db.session.commit()
        return user

    def test_create_user(self):
        user = self.add_dummy_user()

        assert user in db.session

        response = self.client.post(
            '/register',
            json=dict(
                username='Dummy',
                public_id=str(uuid.uuid4()),
                email='dummy@dummy.com',
                password=generate_password_hash('passwd', method='sha256')
            ),
            follow_redirects=True
        )
        assert response.status_code == 409

        response = self.client.post(
            '/register',
            json=dict(
                username='Dummy 2',
                public_id=str(uuid.uuid4()),
                email='dummy2@dummy.com',
                password=generate_password_hash('passwd2', method='sha256')
            ),
            follow_redirects=True
        )
        assert response.status_code == 201


# def test_insert_user(client):
#     res = client.post(
#         '/register',
#         {
#             'username': 'dummy',
#             'email': 'dummy@dummy.com',
#             'password': 'passwd',
#             'public_id': str(uuid.uuid4())
#         }
#     )
#     assert res.status_code == 201
#
#
# def test_empty_db(client):
#     """Start with a blank database."""
#
#     rv = client.get('/')
#     assert b'404' in rv.data


# def test_quote(client):
#     """
#     Test to add a quote.
#
#     :param client: The client
#     """
#     response = client.post(
#         '/quotes',
#         json={
#             'text': 'This is a quote',
#             'author': 'A wise man',
#             'book': 'A good book',
#         }
#     )
#     assert response.status_code == 201
#     response_json = response.get_json()
#     assert response_json['text'] == 'This is a quote'
#     quote_id = response_json['id']
#     assert client.put(f'/quote/{quote_id}', json={'text': 'A modified quote'}).status_code == 200
#     assert client.delete(f'/quote/{quote_id}').status_code == 200
#     assert client.get('/quote/1').status_code == 404
#
#
# def test_get_quotes(client):
#     """
#     Test to get quotes.
#
#     :param client: the client
#     """
#     client.post(
#         '/quotes',
#         json={
#             'text': 'This is a quote',
#             'author': 'A wise man',
#             'book': 'A good book',
#         }
#     )
#     rv = client.get('/quotes').get_json()
#     assert len(rv['quotes']) > 0


if __name__ == '__main__':
    unittest.main()
