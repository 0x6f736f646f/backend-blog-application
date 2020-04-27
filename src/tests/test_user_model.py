import unittest
from base import BaseTestCase
from api import db
from api.models.userModel import UserModel as User


class TestUserModel(BaseTestCase):
    def test_encode_auth_token(self):
        post_data = {'name': "Rodney Osodo",
                     'bio': "Hello",
                     'photo': "http2",
                     'email': "test@gmail.com",
                     'password': "test"}
        user = User(
            post_data
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        post_data = {'name': "Rodney Osodo",
                     'bio': "Hello",
                     'photo': "http2",
                     'email': "test@gmail.com",
                     'password': "test"}
        user = User(
            post_data
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")) == 1)


if __name__ == '__main__':
    unittest.main()
