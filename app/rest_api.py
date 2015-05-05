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


@app.route('/get_user_by_username/<username>', methods=['GET'])
def username_user(username):
    sought_user = get_user_by_username(username)
    result = []
    if sought_user is not None:
        result.append(sought_user.as_dict())
    return json.jsonify({"user": result})


@app.route('/get_posts_by_id/<user_id>', methods=['GET'])
def get_posts_id(user_id):
    posts = get_posts_by_id(user_id)
    result = []
    if posts is not None:
        for post in posts:
            result.append(post.as_dict())
    return json.jsonify({"posts": result})


# returns json on form {"post_ids": [int id1, int id2]}
@app.route('/get_user_likes_by_id/<user_id>', methods=['GET'])
def get_user_likes_id(user_id):
    likes = get_likes_by_id(user_id)
    posts = []
    for like in likes:
        posts.append(like[1])
    return json.jsonify({"post_ids": posts})


# returns json on form {"user_ids": [int id, int id2, int id3]}
@app.route('/get_all_followed_by_id/<user_id>', methods=['GET'])
def get_followed_users_id(user_id):
    followed_users = get_list_of_followed_user_ids(user_id)
    return json.jsonify({"user_ids": followed_users})


@app.route('/get_number_of_likes_for_post/<post_id>', methods=['GET'])
def get_number_of_likes_id(post_id):
    likes = get_all_likes_for_post(post_id)
    number_of_likes = len(likes)
    return json.jsonify({"number_of_likes": str(number_of_likes)})


@app.route('/get_comments_for_post_by_id/<post_id>', methods=['GET'])
def get_comments_for_post(post_id):
    comments = get_comments_for_post_by_id(post_id)
    result = []
    if comments is not None:
        for comment in comments:
            result.append(comment.as_dict())
    return json.jsonify({"comments": result})


@app.route('/get_feed_posts_by_id/<user_id>', methods=['GET'])
def get_user_feed(user_id):
    followed_users = get_list_of_followed_user_ids(user_id)
    user_ids = followed_users + [user_id]
    print(user_ids)
    posts = get_posts_by_multiple_ids(user_ids)
    print(posts)
    result = []
    if posts is not None:
        for post in posts:
            result.append(post.as_dict())
    return json.jsonify({"posts": result})


@app.route('/get_posts_ordered_by_likes', methods=['GET'])
def get_post_top_list():
    posts = get_posts()
    sorted_list = []
    result = []
    for post in posts:
        postid = post.id
        likes = get_all_likes_for_post(postid)
        number_of_likes = len(likes)
        postobj = {"post_id": post.id, "user_id": post.user_id, "artist": post.artist, "title": post.title
                   , "description": post.description, "likes": number_of_likes}
        post_and_number_of_likes_tuple = (postobj, number_of_likes)
        sorted_list = add_post_in_order(sorted_list, post_and_number_of_likes_tuple)
    if len(sorted_list) >= 10:
        sorted_list = sorted_list[0:10]
    for sorted_item in sorted_list:
        result.append(sorted_item[0])
    return json.jsonify({"post_top_list": result})


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
def add_new_comment():
    json_object = request.get_json(force=True)
    data = json_object["comment"][0]
    add_comment(data)
    return json.jsonify({"result": "ok"})


@app.route('/follow/', methods=['POST'])
def do_follow():
    json_object = request.get_json(force=True)
    data = json_object["action"][0]
    follower = data["follower_id"]
    followed = data["followed_id"]
    follow_user(follower, followed)
    return json.jsonify({"result": "followed"})


@app.route('/unfollow/', methods=['POST'])
def do_unfollow():
    json_object = request.get_json(force=True)
    data = json_object["action"][0]
    follower = data["follower_id"]
    followed = data["followed_id"]
    unfollow_user(follower, followed)
    return json.jsonify({"result": "unfollowed"})


@app.route('/like/', methods=['POST'])
def do_like():
    json_object = request.get_json(force=True)
    data = json_object["action"][0]
    user_liking = data["user_id"]
    post = data["post_id"]
    like_post(user_liking, post)
    return json.jsonify({"result": "liked"})


@app.route('/unlike/', methods=['POST'])
def do_unlike():
    json_object = request.get_json(force=True)
    data = json_object["action"][0]
    user_unliking = data["user_id"]
    post = data["post_id"]
    unlike_post(user_unliking, post)
    return json.jsonify({"result": "unliked"})


def get_list_of_followed_user_ids(user_id):
    follow_relations = get_followed_users_by_id(user_id)
    followed_users = []
    for relation in follow_relations:
        followed_users.append(relation[1])
    return followed_users


# Recursive function to sort after number of likes which is the element of index 1 in the tuple
def add_post_in_order(seq, post_tuple):
    if not seq:
        return [post_tuple]
    elif seq[0][1] > post_tuple[1]:
        return [seq[0]] + add_post_in_order(seq[1:], post_tuple)
    else:
        return [post_tuple] + seq




