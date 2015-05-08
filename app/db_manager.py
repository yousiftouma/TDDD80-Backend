__author__ = 'Yousif Touma'

from .models import *
from datetime import datetime
from flask import json
from sqlalchemy import desc


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_users():
    return User.query.all()


def get_posts():
    return SongPost.query.all()


def get_post(post_id):
    return SongPost.query.filter_by(id=post_id).first()


def get_posts_by_id(user_id):
    return SongPost.query.filter_by(user_id=user_id).order_by(desc(SongPost.timestamp)).all()


def get_posts_by_multiple_ids(user_ids):
    return db.session.query(SongPost).filter(SongPost.user_id.in_(user_ids)).order_by(desc(SongPost.timestamp)).all()


def get_likes_by_id(user_id):
    return db.session.query(like_relation).filter(like_relation.c.user_id == user_id).all()


def get_followed_users_by_id(user_id):
    return db.session.query(followers).filter(followers.c.follower_id == user_id).all()


def get_all_likes_for_post(post_id):
    return db.session.query(like_relation).filter(like_relation.c.post_id == post_id).all()


def get_comments_for_post_by_id(post_id):
    return Comment.query.filter_by(song_post_id=post_id).order_by(desc(Comment.timestamp)).all()


def like_post(user, post):
    post_object = SongPost.query.get(post)
    user_object = User.query.get(user)
    if not post_object:
        return json.jsonify({"result": "post id doesn't exist"}), 508
    if not user_object:
        return json.jsonify({"result": "liking user id doesn't exist"}), 509
    relation = post_object.get_liked(user_object)
    if relation:
        db.session.add(relation)
        db.session.commit()
        return json.jsonify({"result": "liked"}), 200
    else:
        return json.jsonify({"result": "already liking"}), 510


def unlike_post(user, post):
    post_object = SongPost.query.get(post)
    user_object = User.query.get(user)
    if not post_object:
        return json.jsonify({"result": "post id doesn't exist"}), 508
    if not user_object:
        return json.jsonify({"result": "liking user id doesn't exist"}), 509
    remove_relation = post_object.get_unliked(user_object)
    if remove_relation:
        db.session.add(remove_relation)
        db.session.commit()
        return json.jsonify({"result": "unliked"}), 200
    else:
        return json.jsonify({"result": "can't unlike if not liking"}), 511


def follow_user(follower, followed):
    follower_user = User.query.get(follower)
    followed_user = User.query.get(followed)
    if not follower_user:
        return json.jsonify({"result": "follower id doesn't exist"}), 505
    if not followed_user:
        return json.jsonify({"result": "followed id doesn't exist"}), 506
    if follower_user == followed_user:
        return json.jsonify({"result": "trying to perform relation with self"}), 507
    relation = follower_user.follow(followed_user)
    if relation:
        db.session.add(relation)
        db.session.commit()
        return json.jsonify({"result": "followed"}), 200
    else:
        return json.jsonify({"result": "already following"}), 503


def unfollow_user(follower, followed):
    follower_user = User.query.get(follower)
    followed_user = User.query.get(followed)
    if not follower_user:
        return json.jsonify({"result": "follower id doesn't exist"}), 505
    if not followed_user:
        return json.jsonify({"result": "followed id doesn't exist"}), 506
    if follower_user == followed_user:
        return json.jsonify({"result": "trying to perform relation with self"}), 507
    remove_relation = follower_user.unfollow(followed_user)
    if remove_relation:
        db.session.add(remove_relation)
        db.session.commit()
        return json.jsonify({"result": "unfollowed"}), 200
    else:
        return json.jsonify({"result": "not following"}), 504


def add_comment(data):
    u = User.query.get(data["user_id"])
    p = SongPost.query.get(data["song_post_id"])
    if not u:
        return json.jsonify({"result": "commenting user doesn't exist"}), 514
    if not p:
        return json.jsonify({"result": "commented post doesn't exist"}), 515
    try:
        assert isinstance(data["text"], str)
        comment = Comment(text=data["text"],
                          timestamp=datetime.utcnow(), comment_author=u, comment_song_post=p)
    except (KeyError, AssertionError) as exception:
        return json.jsonify({"result": "comment wrongly formatted"}), 516
    db.session.add(comment)
    db.session.commit()
    return json.jsonify({"result": "ok"}), 200


def add_song_post(data):
    u = User.query.get(data["user_id"])
    if not u:
        return json.jsonify({"result": "posting user doesn't exist"}), 512
    try:
        assert isinstance(data["title"], str)
        assert isinstance(data["description"], str)
        assert isinstance(data["location"], str)
        assert isinstance(data["mediafile_path"], str)
        song_post = SongPost(post_author=u, title=data["title"], artist=u.username, description=data["description"],
                             timestamp=datetime.utcnow(), mediafile_path=data["mediafile_path"],
                             location=data["location"])
    except (KeyError, AssertionError) as exception:
        return json.jsonify({"result": "post wrongly formatted"}), 513
    db.session.add(song_post)
    db.session.commit()
    return json.jsonify({"result": "ok"}), 200


#return json result plus unique (for errors) status codes used for testing
def add_user(data):
    profile_pic_path = "my default file path"
    if User.query.filter_by(username=data["username"]).first() is not None:
        return json.jsonify({"result": "username taken"}), 501
    elif User.query.filter_by(email=data["email"]).first() is not None:
        return json.jsonify({"result": "email taken"}), 502
    else:
        db.session.add(User(username=data["username"], email=data["email"], password=data["password"],
                            profile_pic=profile_pic_path))
        db.session.commit()
        return json.jsonify({"result": "ok"}), 200



