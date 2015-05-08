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
        db.create_all()

    @app.teardown_appcontext
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_new_user(self):
        """Tests user creation"""

        base_url = 'http://127.0.0.1:4599'

        # user info
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
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        follow1 = json.dumps({"action": [{"follower_id": 1, "followed_id": 2}]})
        follow2 = json.dumps({"action": [{"follower_id": 2, "followed_id": 1}]})
        follow3 = json.dumps({"action": [{"follower_id": 1, "followed_id": 3}]})
        follow4 = json.dumps({"action": [{"follower_id": 4, "followed_id": 1}]})
        follow5 = json.dumps({"action": [{"follower_id": 1, "followed_id": 4}]})
        follow6 = json.dumps({"action": [{"follower_id": 1, "followed_id": 1}]})

        resp = self.client.post(base_url + '/follow/', data=follow1)
        resp2 = self.client.post(base_url + '/follow/', data=follow1)
        resp3 = self.client.post(base_url + '/follow/', data=follow2)
        resp4 = self.client.post(base_url + '/follow/', data=follow3)
        resp5 = self.client.post(base_url + '/follow/', data=follow4)
        resp6 = self.client.post(base_url + '/follow/', data=follow5)
        resp7 = self.client.post(base_url + '/follow/', data=follow6)

        self.assertTrue(resp.status_code == 200)  # Successful follow
        self.assertTrue(resp2.status_code == 503)  # Already following
        self.assertTrue(resp3.status_code == 200)  # Successful follow back
        self.assertTrue(resp4.status_code == 200)  # Successfully following more users
        self.assertTrue(resp5.status_code == 505)  # Follower user doesn't exist
        self.assertTrue(resp6.status_code == 506)  # Followed user doesn't exist
        self.assertTrue(resp7.status_code == 507)  # Trying to follow self

    def test_unfollow(self):
        """Tests unfollowing"""

        base_url = 'http://127.0.0.1:4599'

        u1 = User(username='john', email='john@example.com', profile_pic="source", password="hej")
        u2 = User(username='susan', email='susan@example.com', password="hej", profile_pic="source")
        u3 = User(username="jojje", email="jojje@me.se", password="hoho", profile_pic="soujr")
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        f1 = u1.follow(u2)
        f2 = u1.follow(u3)
        f3 = u2.follow(u1)
        ## u1 follows u2, u1 follows u3, u2 follows u1
        db.session.add(f1)
        db.session.add(f2)
        db.session.add(f3)
        db.session.commit()

        unfollow1 = json.dumps({"action": [{"follower_id": 1, "followed_id": 2}]})
        unfollow2 = json.dumps({"action": [{"follower_id": 2, "followed_id": 1}]})
        unfollow3 = json.dumps({"action": [{"follower_id": 1, "followed_id": 3}]})
        unfollow4 = json.dumps({"action": [{"follower_id": 4, "followed_id": 1}]})
        unfollow5 = json.dumps({"action": [{"follower_id": 1, "followed_id": 4}]})
        unfollow6 = json.dumps({"action": [{"follower_id": 1, "followed_id": 1}]})

        resp = self.client.post(base_url + '/unfollow/', data=unfollow1)
        resp2 = self.client.post(base_url + '/unfollow/', data=unfollow1)
        resp3 = self.client.post(base_url + '/unfollow/', data=unfollow2)
        resp4 = self.client.post(base_url + '/unfollow/', data=unfollow3)
        resp5 = self.client.post(base_url + '/unfollow/', data=unfollow4)
        resp6 = self.client.post(base_url + '/unfollow/', data=unfollow5)
        resp7 = self.client.post(base_url + '/unfollow/', data=unfollow6)

        self.assertTrue(resp.status_code == 200)  # Successful unfollow
        self.assertTrue(resp2.status_code == 504)  # not following user trying to unfollow
        self.assertTrue(resp3.status_code == 200)  # Successful unfollow other user
        self.assertTrue(resp4.status_code == 200)  # Successfully unfollowing
        self.assertTrue(resp5.status_code == 505)  # Follower user doesn't exist
        self.assertTrue(resp6.status_code == 506)  # Followed user doesn't exist
        self.assertTrue(resp7.status_code == 507)  # Trying to unfollow self

    def test_like(self):
        """Tests liking"""

        base_url = 'http://127.0.0.1:4599'

        u1 = User(username='john', email='john@example.com', profile_pic="source", password="hej")
        u2 = User(username='susan', email='susan@example.com', password="hej", profile_pic="source")
        p1 = SongPost(post_author=u1, artist="u1", title="title", description="description",
                      timestamp=datetime.utcnow(), mediafile_path="path", location="Swe")
        p2 = SongPost(post_author=u2, artist="u2", title="title2", description="description2",
                      timestamp=datetime.utcnow(), mediafile_path="path2", location="Sweden")
        db.session.add_all([u1, u2, p1, p2])
        db.session.commit()

        like1 = json.dumps({"action": [{"user_id": 1, "post_id": 1}]})
        like2 = json.dumps({"action": [{"user_id": 1, "post_id": 2}]})
        like3 = json.dumps({"action": [{"user_id": 2, "post_id": 2}]})
        like4 = json.dumps({"action": [{"user_id": 3, "post_id": 2}]})
        like5 = json.dumps({"action": [{"user_id": 2, "post_id": 3}]})

        resp = self.client.post(base_url + '/like/', data=like1)
        resp2 = self.client.post(base_url + '/like/', data=like1)
        resp3 = self.client.post(base_url + '/like/', data=like2)
        resp4 = self.client.post(base_url + '/like/', data=like3)
        resp5 = self.client.post(base_url + '/like/', data=like4)
        resp6 = self.client.post(base_url + '/like/', data=like5)

        self.assertTrue(resp.status_code == 200)  # Successful like (and users own post)
        self.assertTrue(resp2.status_code == 510)  # Trying to like a post already liked by self
        self.assertTrue(resp3.status_code == 200)  # Successfully like more than one post
        self.assertTrue(resp4.status_code == 200)  # Successfully like post already liked by someone else
        self.assertTrue(resp5.status_code == 509)  # user doesn't exist
        self.assertTrue(resp6.status_code == 508)  # post doesn't exist

    def test_unlike(self):
        """Tests unliking"""

        base_url = 'http://127.0.0.1:4599'

        u1 = User(username='john', email='john@example.com', profile_pic="source", password="hej")
        u2 = User(username='susan', email='susan@example.com', password="hej", profile_pic="source")
        p1 = SongPost(post_author=u1, artist="u1", title="title", description="description",
                      timestamp=datetime.utcnow(), mediafile_path="path", location="Swe")
        p2 = SongPost(post_author=u2, artist="u2", title="title2", description="description2",
                      timestamp=datetime.utcnow(), mediafile_path="path2", location="Sweden")
        db.session.add_all([u1, u2, p1, p2])
        db.session.commit()

        like1 = p1.get_liked(u1)  # u1 likes p1
        like2 = p1.get_liked(u2)  # u2 likes p1
        like3 = p2.get_liked(u1)  # u1 likes p2

        db.session.add_all([like1, like2, like3])

        unlike1 = json.dumps({"action": [{"user_id": 1, "post_id": 1}]})
        unlike2 = json.dumps({"action": [{"user_id": 1, "post_id": 2}]})
        unlike3 = json.dumps({"action": [{"user_id": 2, "post_id": 1}]})
        unlike4 = json.dumps({"action": [{"user_id": 2, "post_id": 2}]})
        unlike5 = json.dumps({"action": [{"user_id": 3, "post_id": 2}]})
        unlike6 = json.dumps({"action": [{"user_id": 2, "post_id": 3}]})

        resp = self.client.post(base_url + '/unlike/', data=unlike1)
        resp2 = self.client.post(base_url + '/unlike/', data=unlike1)
        resp3 = self.client.post(base_url + '/unlike/', data=unlike2)
        resp4 = self.client.post(base_url + '/unlike/', data=unlike3)
        resp5 = self.client.post(base_url + '/unlike/', data=unlike4)
        resp6 = self.client.post(base_url + '/unlike/', data=unlike5)
        resp7 = self.client.post(base_url + '/unlike/', data=unlike6)

        self.assertTrue(resp.status_code == 200)  # Successful unlike of own post
        self.assertTrue(resp2.status_code == 511)  # Trying to unlike post not liked
        self.assertTrue(resp3.status_code == 200)  # Successfully unlike of others post
        self.assertTrue(resp4.status_code == 200)  # Successfully unlike post
        self.assertTrue(resp5.status_code == 511)  # Trying to unlike post not liked
        self.assertTrue(resp6.status_code == 509)  # user doesn't exist
        self.assertTrue(resp7.status_code == 508)  # post doesn't exist

    def test_post(self):
        """Testing post creation"""

        base_url = 'http://127.0.0.1:4599'

        u1 = User(username='john', email='john@example.com', profile_pic="source", password="hej")
        db.session.add(u1)
        db.session.commit()

        # create a user
        user_id1 = 1
        user_id2 = 2
        title = 'fool'
        description = 'bar'
        mediafile_path = "path"
        location = "swe"

        post1 = json.dumps({"song_post": [{'user_id': user_id1, 'title': title, 'description': description
                                           , "mediafile_path": mediafile_path, "location": location}]})
        post2 = json.dumps({"song_post": [{'user_id': user_id2, 'title': title, 'description': description
                                           , "mediafile_path": mediafile_path, "location": location}]})
        post3 = json.dumps({"song_post": [{'user_id': user_id1, 'title': title, 'description': description
                                           , "mediafile_path": mediafile_path}]})
        post4 = json.dumps({"song_post": [{'user_id': user_id1, 'title': 1, 'description': description
                                           , "mediafile_path": mediafile_path, "location": location}]})

        resp = self.client.post(base_url + '/add_post', data=post1)
        resp2 = self.client.post(base_url + '/add_post', data=post2)
        resp3 = self.client.post(base_url + '/add_post', data=post3)
        resp4 = self.client.post(base_url + '/add_post', data=post1)
        resp5 = self.client.post(base_url + '/add_post', data=post4)

        self.assertTrue(resp.status_code == 200)  # Successful creation
        self.assertTrue(resp2.status_code == 512)  # Non existing user trying to add post
        self.assertTrue(resp3.status_code == 513)  # Missing information in json object
        self.assertTrue(resp4.status_code == 200)  # can create another post with same info
        self.assertTrue(resp5.status_code == 513)  # sending int instead of string as title (wrong format)

    def test_comment(self):
        """Testing commenting post"""

        base_url = 'http://127.0.0.1:4599'

        u1 = User(username='john', email='john@example.com', profile_pic="source", password="hej")
        p1 = SongPost(post_author=u1, artist="u1", title="title", description="description",
                      timestamp=datetime.utcnow(), mediafile_path="path", location="Swe")

        db.session.add_all([u1, p1])
        db.session.commit()

        comment1 = json.dumps({"comment": [{'user_id': 1, "song_post_id": 1, "text": "hej"}]})
        comment2 = json.dumps({"comment": [{'user_id': 1, "song_post_id": 1, "text": 1}]})
        comment3 = json.dumps({"comment": [{'user_id': 2, "song_post_id": 1, "text": "hej"}]})
        comment4 = json.dumps({"comment": [{'user_id': 1, "song_post_id": 2, "text": "hej"}]})
        comment5 = json.dumps({"comment": [{'user_id': 1, "song_post_id": 1}]})

        resp = self.client.post(base_url + '/add_comment', data=comment1)
        resp2 = self.client.post(base_url + '/add_comment', data=comment1)
        resp3 = self.client.post(base_url + '/add_comment', data=comment2)
        resp4 = self.client.post(base_url + '/add_comment', data=comment3)
        resp5 = self.client.post(base_url + '/add_comment', data=comment4)
        resp6 = self.client.post(base_url + '/add_comment', data=comment5)

        self.assertTrue(resp.status_code == 200)  # Successful comment
        self.assertTrue(resp2.status_code == 200)  # Successful comment again
        self.assertTrue(resp3.status_code == 516)  # Text is int, not string
        self.assertTrue(resp4.status_code == 514)  # User commenting not existing
        self.assertTrue(resp5.status_code == 515)  # Post commented not existing
        self.assertTrue(resp6.status_code == 516)  # Missing info in json object

    def test_get_most_liked_posts(self):
        """Testing the most liked top list getter for posts"""

        base_url = 'http://127.0.0.1:4599'

        u1 = User(username='john', email='john@example.com', profile_pic="source", password="hej")
        u2 = User(username='susan', email='susan@example.com', password="hej", profile_pic="source")
        p1 = SongPost(post_author=u1, artist="u1", title="title", description="description",
                      timestamp=datetime.utcnow(), mediafile_path="path", location="Swe")
        p2 = SongPost(post_author=u2, artist="u2", title="title2", description="description2",
                      timestamp=datetime.utcnow(), mediafile_path="path2", location="Sweden")
        p3 = SongPost(post_author=u2, artist="u2", title="title3", description="description3",
                      timestamp=datetime.utcnow(), mediafile_path="path3", location="Swedens")

        db.session.add_all([u1, u2, p1, p2, p3])
        db.session.commit()

        l1 = p1.get_liked(u1)
        l2 = p1.get_liked(u2)
        l3 = p3.get_liked(u1)

        db.session.add_all([l1, l2, l3])
        db.session.commit()

        # Now the first added post has 2 likes, second has 0 and third has 1
        # normally, they would be "sorted" as latest post on "top" so order would be 3, 2, 1
        # we want to test that it's sorted by likes, i.e. 1, 3, 2

        resp = self.client.get(base_url + '/get_posts_ordered_by_likes')
        response_loaded = json.loads(resp.data)

        exp_top = {"id": 1, "artist": "u1", "title": "title", "description": "description",
                             "likes": 2, "location": "Swe", "user_id": 1}
        exp_last = {"id": 2, "artist": "u2", "title": "title2", "description": "description2",
                                "likes": 0, "location": "Sweden", "user_id": 2}
        exp_sec = {"id": 3, "artist": "u2", "title": "title3", "description": "description3",
                              "likes": 1, "location": "Swedens", "user_id": 2}
        exp_json_arr = [exp_top, exp_sec, exp_last]
        exp_json_obj = {"post_top_list": exp_json_arr}

        self.assertTrue(response_loaded == exp_json_obj)


if __name__ == '__main__':
    unittest.main()