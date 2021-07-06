#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
import pytest
from pmhcmdsapp.app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////users/brendon/dev/testdb/h2h.db'


@pytest.fixture
def client():
    app = create_app(TestConfig)

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


# class UserModelCase(pytest.TestCase):
#     def setUp(self):
#         self.app = create_app(TestConfig)
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

#     def test_password_hashing(self):
#         u = User(email='brian@gmail.com')
#         u.set_password('cat')
#         self.assertFalse(u.check_password('dog'))
#         self.assertTrue(u.check_password('cat'))

# @pytest.fixture(autouse=True)
# def app_context(app):
#     """Creates a flask app context"""
#     with app.app_context():
#         yield app



# @pytest.fixture(autouse=True)
# def app():
#     """Create application for the tests."""
#     _app = create_app(TestConfig)
#     _app.logger.setLevel(logging.CRITICAL)
#     ctx = _app.test_request_context()
#     ctx.push()

#     yield _app

#     ctx.pop()



# @pytest.fixture(scope="model")
# def db(app_context):

#     db.create_all()

#     # seed the database
#     # seed_db()

#     yield db

#     # teardown database
#     # https://stackoverflow.com/a/18365654/5819113
#     # db.session.remove()
#     # db.drop_all()
#     # db.get_engine(app_context).dispose()


# @pytest.mark.usefixtures("db")
# class TestUser:
#     """User tests."""

#     def test_get_by_id(self):
#         """Get user by ID."""
#         user = User("foo", "foo@bar.com")
#         user.save()

#         retrieved = User.get_by_id(user.id)
#         assert retrieved == user


