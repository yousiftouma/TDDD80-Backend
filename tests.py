__author__ = 'Yousif Touma'

# !flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import *
from datetime import datetime


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_follow(self):
        u1 = User(username='john', email='john@example.com', profile_pic="source", password="hej")
        u2 = User(username='susan', email='susan@example.com', password="hej", profile_pic="source")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().username == 'susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().username == 'john'
        u = u1.unfollow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    def test_like(self):
        u1 = User(username='john', email='john@example.com', profile_pic="source", password="hej")
        p1 = SongPost(post_author=u1, artist="u1", title="title", description="description",
                      timestamp=datetime.utcnow(), mediafile_path="path")
        db.session.add(u1)
        db.session.add(p1)
        db.session.commit()
        assert p1.get_unliked(u1) is None
        l = p1.get_liked(u1)
        db.session.add(l)
        db.session.commit()
        assert p1.get_liked(u1) is None
        assert p1.is_liked_by(u1)
        assert p1.likes.count() == 1
        assert p1.likes.first().username == 'john'
        post_id = db.session.query(like_relation).filter(like_relation.c.user_id == 1).first().post_id
        user_id = db.session.query(like_relation).filter(like_relation.c.user_id == 1).first().user_id
        post = SongPost.query.get(post_id)
        user = User.query.get(user_id)
        assert user.id == 1
        assert user.username == "john"
        assert post.id == 1
        assert post.title == "title"
        test = db.session.query(like_relation).filter(like_relation.c.user_id == 1).all()
        print("user_id, post_id -" + " list= ", test)
        #assert u1.like_relation.count() == 1
        #assert u1.like_relation.first().title == 'title'
        # ul = p1.get_unliked(u1)
        # assert ul is not None
        # db.session.add(ul)
        # db.session.commit()
        # assert not p1.is_liked_by(u1)
        # assert p1.likes.count() == 0
        #assert u1.like_relation.count() == 0


if __name__ == '__main__':
    unittest.main()