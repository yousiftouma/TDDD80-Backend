__author__ = 'Yousif Touma'

# !flask/bin/python
import os
import unittest

from flask import json, Flask
from flask.ext.testing import TestCase
from config import basedir
from app import app, db
from app.models import *
from datetime import datetime


class ApiTest(TestCase):

    def create_app(self):
        """Required method. Always implement this so that app is returned with context."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        context = app.app_context()
        context.push()
        return app

    def setUp(self):
        #self.app = app.test_client()
        db.create_all()

    @app.teardown_appcontext
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_new_user(self):
        """Tests user creation"""

        base_url = 'http://127.0.0.1:4599'

        # create a user
        username = 'foo'
        username2 = 'fool'
        password = 'bar'
        email = "yousif@y.com"
        email2 = "yousif@ya.com"

        user1 = json.dumps({"user": [{'email': email, 'username': username, 'password': password}]})
        user2 = json.dumps({"user": [{'email': email, 'username': username2, 'password': password}]})
        user3 = json.dumps({"user": [{'email': email2, 'username': username, 'password': password}]})

        resp = self.client.post(base_url + '/register_user', data=user1)
        resp2 = self.client.post(base_url + '/register_user', data=user2)
        resp3 = self.client.post(base_url + '/register_user', data=user3)

        self.assertTrue(resp.status_code == 200)  # Successful creation
        self.assertTrue(resp2.status_code == 502)  # email taken
        self.assertTrue(resp3.status_code == 501)  # username taken

    def test_follow(self):
        """Tests following"""

        base_url = 'http://127.0.0.1:4599'

        u1 = User(username='john', email='john@example.com', profile_pic="source", password="hej")
        u2 = User(username='susan', email='susan@example.com', password="hej", profile_pic="source")
        u3 = User(username="jojje", email="jojje@me.se", password="hoho", profile_pic="soujr")
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()

        follow1 = json.dumps({"action": [{"follower_id": 1, "followed_id": 2}]})
        follow2 = json.dumps({"action": [{"follower_id": 2, "followed_id": 1}]})
        follow3 = json.dumps({"action": [{"follower_id": 1, "followed_id": 3}]})

        resp = self.client.post(base_url + '/follow/', data=follow1)
        resp2 = self.client.post(base_url + '/follow/', data=follow1)
        resp3 = self.client.post(base_url + '/follow/', data=follow2)
        resp4 = self.client.post(base_url + '/follow/', data=follow3)

        self.assertTrue(resp.status_code == 200)  # Successful follow
        self.assertTrue(resp2.status_code == 503)  # Already following
        self.assertTrue(resp3.status_code == 200)  # Successful follow back
        self.assertTrue(resp4.status_code == 200)  # Successfully following more users

    # def test_like(self):
    #     u1 = User(username='john', email='john@example.com', profile_pic="source", password="hej")
    #     p1 = SongPost(post_author=u1, artist="u1", title="title", description="description",
    #                   timestamp=datetime.utcnow(), mediafile_path="path")
    #     db.session.add(u1)
    #     db.session.add(p1)
    #     db.session.commit()
    #     assert p1.get_unliked(u1) is None
    #     l = p1.get_liked(u1)
    #     db.session.add(l)
    #     db.session.commit()
    #     assert p1.get_liked(u1) is None
    #     assert p1.is_liked_by(u1)
    #     assert p1.likes.count() == 1
    #     assert p1.likes.first().username == 'john'
    #     post_id = db.session.query(like_relation).filter(like_relation.c.user_id == 1).first().post_id
    #     user_id = db.session.query(like_relation).filter(like_relation.c.user_id == 1).first().user_id
    #     post = SongPost.query.get(post_id)
    #     user = User.query.get(user_id)
    #     assert user.id == 1
    #     assert user.username == "john"
    #     assert post.id == 1
    #     assert post.title == "title"
    #     test = db.session.query(like_relation).filter(like_relation.c.user_id == 1).all()
    #     print("user_id, post_id -" + " list= ", test)

if __name__ == '__main__':
    unittest.main()