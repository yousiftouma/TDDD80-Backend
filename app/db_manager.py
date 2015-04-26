__author__ = 'Yousif Touma'

from .models import *
from datetime import datetime
from flask import json
from sqlalchemy import desc


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_users():
    return User.query.all()


def get_post(post_id):
    return SongPost.query.filter_by(id=post_id).first()


def get_posts_by_id(user_id):
    return SongPost.query.filter_by(user_id=user_id).order_by(desc(SongPost.timestamp)).all()


def get_likes_by_id(user_id):
    return db.session.query(like_relation).filter(like_relation.c.user_id == user_id).all()


def get_all_likes_for_post(post_id):
    return db.session.query(like_relation).filter(like_relation.c.post_id == post_id).all()


def get_comments_for_post_by_id(post_id):
    print("getting comments in db manager")
    return Comment.query.filter_by(song_post_id=post_id).order_by(desc(Comment.timestamp)).all()


def like_post(user, post):
    postObj = SongPost.query.get(post)
    userObj = User.query.get(user)
    relation = postObj.get_liked(userObj)
    db.session.add(relation)
    db.session.commit()


def unlike_post(user, post):
    postObj = SongPost.query.get(post)
    userObj = User.query.get(user)
    remove_relation = postObj.get_unliked(userObj)
    db.session.add(remove_relation)
    db.session.commit()


def follow_user(follower, followed):
    follower_user = User.query.get(follower)
    followed_user = User.query.get(followed)
    relation = follower_user.follow(followed_user)
    db.session.add(relation)
    db.session.commit()


def unfollow_user(follower, followed):
    follower_user = User.query.get(follower)
    followed_user = User.query.get(followed)
    remove_relation = follower_user.unfollow(followed_user)
    db.session.add(remove_relation)
    db.session.commit()


def add_comment(data):
    u = User.query.get(data["user_id"])
    p = SongPost.query.get(data["song_post_id"])
    comment = Comment(text=data["text"],
                      timestamp=datetime.utcnow(), comment_author=u, comment_song_post=p)
    db.session.add(comment)
    db.session.commit()


def add_song_post(data):
    u = User.query.get(data["user_id"])
    song_post = SongPost(post_author=u, title=data["title"], artist=u.username, description=data["description"],
                         timestamp=datetime.utcnow(), mediafile_path=data["mediafile_path"])
    db.session.add(song_post)
    db.session.commit()


def add_user(data):
    profile_pic_path = "my default file path"
    if User.query.filter_by(username=data["username"]).first() is not None:
        return json.jsonify({"result": "username taken"})
    elif User.query.filter_by(email=data["email"]).first() is not None:
        return json.jsonify({"result": "email taken"})
    else:
        db.session.add(User(username=data["username"], email=data["email"], password=data["password"],
                            profile_pic=profile_pic_path))
        db.session.commit()
        return json.jsonify({"result": "ok"})



