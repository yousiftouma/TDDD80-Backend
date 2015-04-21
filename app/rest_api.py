__author__ = 'Yousif Touma'

from app import app, db
from flask import json, request, session, g
from app.db_manager import *


@app.errorhandler(404)
def not_found_error(error):
    error_dict = {"code": 404,
                  "message": "file not found"}
    return json.jsonify(error_dict)


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    error_dict = {"code": 500,
                  "message": "database error"}
    return json.jsonify(error_dict)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/get_users', methods=['GET'])
def users():
    all_users = get_users()
    result = []
    if all_users is not None:
        for cur_user in all_users:
            result.append(cur_user.as_dict())
    return json.jsonify({"users": result})


@app.route('/get_user_by_email/<email>', methods=['GET'])
def email_user(email):
    sought_user = get_user_by_email(email)
    result = []
    if sought_user is not None:
        result.append(sought_user.as_dict())
    return json.jsonify({"user": result})


@app.route('/get_user_by_id/<id>', methods=['GET'])
def id_user(id):
    sought_user = get_user_by_id(id)
    result = []
    if sought_user is not None:
        result.append(sought_user.as_dict())
    return json.jsonify({"user": result})


@app.route('/get_posts_by_id/<user_id>', methods=['GET'])
def get_posts(user_id):
    posts = get_posts_by_id(user_id)
    result = []
    if posts is not None:
        for post in posts:
            result.append(post.as_dict())
    return json.jsonify({"posts": result})


@app.route('/get_user_likes_by_id/<user_id>', methods=['GET'])
def get_user_likes(user_id):
    likes = get_likes_by_id(user_id)
    print("hej")
    return likes


@app.route('/register_user', methods=['POST'])
def register_user():
    json_object = request.get_json(force=True)
    data = json_object["user"][0]
    return add_user(data)


@app.route('/add_post', methods=['POST'])
def add_post():
    json_object = request.get_json(force=True)
    data = json_object["song_post"][0]
    add_song_post(data)
    return json.jsonify({"result": "ok"})


@app.route('/add_comment', methods=['POST'])
def add_cmnt():
    json_object = request.get_json(force=True)
    data = json_object["comment"][0]
    add_comment(data)
    return json.jsonify({"result": "ok"})


@app.route('/follow/', methods=['POST'])
def do_follow():
    follower = get_user_by_id(request.args.get('follower'))
    followed = get_user_by_id(request.args.get('followed'))
    follow_user(follower, followed)
    return json.jsonify({"result": "ok"})


@app.route('/unfollow/', methods=['POST'])
def do_unfollow():
    follower = get_user_by_id(request.args.get('follower'))
    followed = get_user_by_id(request.args.get('followed'))
    unfollow_user(follower, followed)
    return json.jsonify({"result": "ok"})


@app.route('/like/', methods=['POST'])
def do_like():
    user_liking = get_user_by_id(request.args.get('liker'))
    post = get_post(request.args.get('post_id'))
    like_post(user_liking, post)
    return json.jsonify({"result": "ok"})


@app.route('/unlike/', methods=['POST'])
def do_unlike():
    user_unliking = get_user_by_id(request.args.get('unliker'))
    post = get_post(request.args.get('post_id'))
    unlike_post(user_unliking, post)
    return json.jsonify({"result": "ok"})




