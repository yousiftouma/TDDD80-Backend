__author__ = 'Yousif Touma'

from app import db

# Relation-table for following, first column is who follows, second column is who is followed
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


# Model to represent user.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    profile_pic = db.Column(db.String)

    # Relation with SongPost, a post will have reference to a user through id
    posts = db.relationship('SongPost', backref=db.backref('post_author', lazy='select'))
    # Same as with posts
    comments = db.relationship('Comment', backref=db.backref('comment_author', lazy='select'))
    # The user will have access to the followers table as both primary and secondary reference
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, username, email, password, profile_pic):
        self.username = username
        self.email = email
        self.password = password
        self.profile_pic = profile_pic

    # How the object will print itself, used for debugging mainly
    def __repr__(self):
        return '<User %r>' % self.username

    # Will return user object as python dict with each column as key and with corresponding data
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    # A user can follow a second user if it isn't following already, adding the followed user
    # to its instance of followed table
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    # Same as above but vice-versa
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    # A method to check if user is already following param user
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

# Relation-table for a user liking a post
like_relation = db.Table('likes',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('post_id', db.Integer, db.ForeignKey('song_post.id')))


# Model to represent a post
class SongPost(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    artist = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    mediafile_path = db.Column(db.String)
    location = db.Column(db.String)

    # A post has a reference in a comment
    comments = db.relationship('Comment', backref=db.backref('comment_song_post', lazy='select'))
    # A post has a relation with user in regards to likes, using the likes table to represent it
    likes = db.relationship('User', secondary=like_relation,
                            backref=db.backref('liked_song_post', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<SongPost %r>' % self.title

    # Return self as a python dict with all columns as keys with corresponding data
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    # A post can get liked by a user if it is not already liked
    def get_liked(self, user):
        if not self.is_liked_by(user):
            self.likes.append(user)
            return self

    # Same as above but vice-versa
    def get_unliked(self, user):
        if self.is_liked_by(user):
            self.likes.remove(user)
            return self

    # Checks if a specific user already likes this post
    def is_liked_by(self, user):
        return self.likes.filter(like_relation.c.user_id == user.id).count() > 0


# Model representing a comment
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # this column is a reference to the user commenting
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # this column is a reference to the post commented
    song_post_id = db.Column(db.Integer, db.ForeignKey('song_post.id'))
    text = db.Column(db.String)
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Comment %r>' % self.text

    # Can return self as python dict with each column as key with corresponding data
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
