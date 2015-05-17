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


# returns all posts by a user, sorted by date, most recent first
def get_posts_by_id(user_id):
    return SongPost.query.filter_by(user_id=user_id).order_by(desc(SongPost.timestamp)).all()


# returns all posts except the ones made by user sent as arg
def get_all_but_my_posts(user_id):
    return SongPost.query.filter(SongPost.user_id != user_id).all()


# Takes a list of ids and returns all posts by those users
def get_posts_by_multiple_ids(user_ids):
    return db.session.query(SongPost).filter(SongPost.user_id.in_(user_ids)).order_by(desc(SongPost.timestamp)).all()


# returns all (user, post) relations where user sent as arg is present
def get_likes_by_id(user_id):
    return db.session.query(like_relation).filter(like_relation.c.user_id == user_id).all()


# returns all (follower, followed) relations where follower is user sent as arg
def get_followed_users_by_id(user_id):
    return db.session.query(followers).filter(followers.c.follower_id == user_id).all()


# returns all (follower, followed) relations where followed is user sent as arg
def get_following_users_by_id(user_id):
    return db.session.query(followers).filter(followers.c.followed_id == user_id).all()


# returns all (user, post) relations where post sent as arg is present
def get_all_likes_for_post(post_id):
    return db.session.query(like_relation).filter(like_relation.c.post_id == post_id).all()


# returns all comments where backreference to the post sent as arg is present
def get_comments_for_post_by_id(post_id):
    return Comment.query.filter_by(song_post_id=post_id).order_by(desc(Comment.timestamp)).all()


# likes a post if all checks are passed, otherwise returns a message and unique error code
# returns ok status code and message if ok
def like_post(user, post):
    post_object = SongPost.query.get(post)
    user_object = User.query.get(user)
    if post_object is None:
        return json.jsonify({"result": "post id doesn't exist"}), 508
    if user_object is None:
        return json.jsonify({"result": "liking user id doesn't exist"}), 509
    relation = post_object.get_liked(user_object)
    # relation will be None if cannot perform it, and cannot perform it means it exists already
    # as we know both objects we are trying to perform it with really exist by this stage
    if relation is None:
        return json.jsonify({"result": "already liking"}), 510
    else:
        db.session.add(relation)
        db.session.commit()
        return json.jsonify({"result": "liked"}), 200


# Same as above but unlike
def unlike_post(user, post):
    post_object = SongPost.query.get(post)
    user_object = User.query.get(user)
    if post_object is None:
        return json.jsonify({"result": "post id doesn't exist"}), 508
    if user_object is None:
        return json.jsonify({"result": "liking user id doesn't exist"}), 509
    remove_relation = post_object.get_unliked(user_object)
    if remove_relation is None:
        return json.jsonify({"result": "can't unlike if not liking"}), 511
    else:
        db.session.add(remove_relation)
        db.session.commit()
        return json.jsonify({"result": "unliked"}), 200


# Same as above but follow
def follow_user(follower, followed):
    follower_user = User.query.get(follower)
    followed_user = User.query.get(followed)
    if follower_user is None:
        return json.jsonify({"result": "follower id doesn't exist"}), 505
    if followed_user is None:
        return json.jsonify({"result": "followed id doesn't exist"}), 506
    if follower_user == followed_user:
        return json.jsonify({"result": "trying to follow/unfollow self"}), 507
    relation = follower_user.follow(followed_user)
    if relation is None:
        return json.jsonify({"result": "already following"}), 503
    else:
        db.session.add(relation)
        db.session.commit()
        return json.jsonify({"result": "followed"}), 200


# Same as above but unfollow
def unfollow_user(follower, followed):
    follower_user = User.query.get(follower)
    followed_user = User.query.get(followed)
    if follower_user is None:
        return json.jsonify({"result": "follower id doesn't exist"}), 505
    if followed_user is None:
        return json.jsonify({"result": "followed id doesn't exist"}), 506
    if follower_user == followed_user:
        return json.jsonify({"result": "trying to follow/unfollow self"}), 507
    remove_relation = follower_user.unfollow(followed_user)
    if remove_relation is None:
        return json.jsonify({"result": "not following"}), 504
    else:
        db.session.add(remove_relation)
        db.session.commit()
        return json.jsonify({"result": "unfollowed"}), 200


# Tries to add a comment,
def add_comment(data):
    user_object = User.query.get(data["user_id"])
    post_object = SongPost.query.get(data["song_post_id"])
    if user_object is None:
        return json.jsonify({"result": "commenting user doesn't exist"}), 514
    if post_object is None:
        return json.jsonify({"result": "commented post doesn't exist"}), 515
    # Checks for formatting errors in the comment
    try:
        assert isinstance(data["text"], str)
        comment = Comment(text=data["text"],
                          timestamp=datetime.utcnow(), comment_author=user_object, comment_song_post=post_object)
    except (KeyError, AssertionError) as exception:
        return json.jsonify({"result": "comment wrongly formatted"}), 516
    db.session.add(comment)
    db.session.commit()
    return json.jsonify({"result": "ok"}), 200


# Same as above but post
def add_song_post(data):
    user_object = User.query.get(data["user_id"])
    if user_object is None:
        return json.jsonify({"result": "posting user doesn't exist"}), 512
    # Checks for formatting errors in the post
    try:
        assert isinstance(data["title"], str)
        assert isinstance(data["description"], str)
        assert isinstance(data["location"], str)
        assert isinstance(data["mediafile_path"], str)
        song_post = SongPost(post_author=user_object, title=data["title"], artist=user_object.username, description=data["description"],
                             timestamp=datetime.utcnow(), mediafile_path=data["mediafile_path"],
                             location=data["location"])
    except (KeyError, AssertionError) as exception:
        return json.jsonify({"result": "post wrongly formatted"}), 513
    db.session.add(song_post)
    db.session.commit()
    return json.jsonify({"result": "ok"}), 200


# return json result plus unique (for errors) status codes
# Adds a user if checks pass
def add_user(data):
    profile_pic_path = "my default file path"
    # Checks if there is a username like this already
    if User.query.filter_by(username=data["username"]).first() is not None:
        return json.jsonify({"result": "username taken"}), 501
    # Same as above but email
    elif User.query.filter_by(email=data["email"]).first() is not None:
        return json.jsonify({"result": "email taken"}), 502
    # Everything seems fine and we add the user
    else:
        db.session.add(User(username=data["username"], email=data["email"], password=data["password"],
                            profile_pic=profile_pic_path))
        db.session.commit()
        return json.jsonify({"result": "ok"}), 200



