__author__ = 'Yousif Touma'

from app import db

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    profile_pic = db.Column(db.String)

    posts = db.relationship('SongPost', backref=db.backref('post_author', lazy='select'))
    comments = db.relationship('Comment', backref=db.backref('comment_author', lazy='select'))
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

    def __repr__(self):
        return '<User %r>' % self.username

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0


like_relation = db.Table('likes',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('post_id', db.Integer, db.ForeignKey('song_post.id')))


class SongPost(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    artist = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    mediafile_path = db.Column(db.String)

    comments = db.relationship('Comment', backref=db.backref('comment_song_post', lazy='select'))
    likes = db.relationship('User', secondary=like_relation,
                            backref=db.backref('liked_song_post', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<SongPost %r>' % self.title

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def get_liked(self, user):
        if not self.is_liked_by(user):
            self.likes.append(user)
            return self

    def get_unliked(self, user):
        if self.is_liked_by(user):
            self.likes.remove(user)
            return self

    def is_liked_by(self, user):
        return self.likes.filter(like_relation.c.user_id == user.id).count() > 0


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_post_id = db.Column(db.Integer, db.ForeignKey('song_post.id'))
    text = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    

    def __repr__(self):
        return '<Comment %r>' % self.text

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
