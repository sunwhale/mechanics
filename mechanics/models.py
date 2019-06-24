# -*- coding: utf-8 -*-
"""
    :author: Jingyu Sun
    :url: http://sunjingyu.com
    :copyright: © 2019 Jingyu Sun <sun.jingyu@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
import os
from datetime import datetime

from flask import current_app
from flask_avatars import Identicon
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from mechanics.extensions import db, whooshee

# relationship table
roles_permissions = db.Table('roles_permissions',
                             db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
                             )


groups_experiments = db.Table('groups_experiments',
                             db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
                             db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id'))
                             )


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'Locked': ['FOLLOW', 'COLLECT'],
            'User': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD'],
            'Moderator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE'],
            'Administrator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE', 'ADMINISTER']
        }

        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()


# relationship object
class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='following', lazy='joined')
    followed = db.relationship('User', foreign_keys=[followed_id], back_populates='followers', lazy='joined')


# relationship object
class Collect(db.Model):
    collector_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                             primary_key=True)
    collected_id = db.Column(db.Integer, db.ForeignKey('photo.id'),
                             primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    collector = db.relationship('User', back_populates='collections', lazy='joined')
    collected = db.relationship('Photo', back_populates='collectors', lazy='joined')


@whooshee.register_model('name', 'username')
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    location = db.Column(db.String(50))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))
    avatar_raw = db.Column(db.String(64))

    confirmed = db.Column(db.Boolean, default=False)
    locked = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    public_collections = db.Column(db.Boolean, default=True)
    receive_comment_notification = db.Column(db.Boolean, default=True)
    receive_follow_notification = db.Column(db.Boolean, default=True)
    receive_collect_notification = db.Column(db.Boolean, default=True)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    role = db.relationship('Role', back_populates='users')
    photos = db.relationship('Photo', back_populates='author', cascade='all')
    comments = db.relationship('Comment', back_populates='author', cascade='all')
    notifications = db.relationship('Notification', back_populates='receiver', cascade='all')
    collections = db.relationship('Collect', back_populates='collector', cascade='all')
    experiments = db.relationship('Experiment', back_populates='author', cascade='all')
    groups = db.relationship('Group', back_populates='author', cascade='all')
    materials = db.relationship('Material', back_populates='author', cascade='all')
    extensometers = db.relationship('Extensometer', back_populates='author', cascade='all')
    geometries = db.relationship('Geometry', back_populates='author', cascade='all')
    following = db.relationship('Follow', foreign_keys=[Follow.follower_id], back_populates='follower',
                                lazy='dynamic', cascade='all')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], back_populates='followed',
                                lazy='dynamic', cascade='all')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_avatar()
        self.follow(self)  # follow self
        self.set_role()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_role(self):
        if self.role is None:
            if self.email == current_app.config['MECHANICS_ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()
            db.session.commit()

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)
            db.session.commit()

    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()

    def is_following(self, user):
        if user.id is None:  # when follow self, user.id will be None
            return False
        return self.following.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    @property
    def followed_photos(self):
        return Photo.query.join(Follow, Follow.followed_id == Photo.author_id).filter(Follow.follower_id == self.id)

    def collect(self, photo):
        if not self.is_collecting(photo):
            collect = Collect(collector=self, collected=photo)
            db.session.add(collect)
            db.session.commit()

    def uncollect(self, photo):
        collect = Collect.query.with_parent(self).filter_by(collected_id=photo.id).first()
        if collect:
            db.session.delete(collect)
            db.session.commit()

    def is_collecting(self, photo):
        return Collect.query.with_parent(self).filter_by(collected_id=photo.id).first() is not None

    def lock(self):
        self.locked = True
        self.role = Role.query.filter_by(name='Locked').first()
        db.session.commit()

    def unlock(self):
        self.locked = False
        self.role = Role.query.filter_by(name='User').first()
        db.session.commit()

    def block(self):
        self.active = False
        db.session.commit()

    def unblock(self):
        self.active = True
        db.session.commit()

    def generate_avatar(self):
        avatar = Identicon()
        filenames = avatar.generate(text=self.username)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()

    @property
    def is_admin(self):
        return self.role.name == 'Administrator'

    @property
    def is_active(self):
        return self.active

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and permission in self.role.permissions


tagging = db.Table('tagging',
                   db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
                   db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                   )


@whooshee.register_model('description')
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    filename = db.Column(db.String(64))
    filename_s = db.Column(db.String(64))
    filename_m = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)
    flag = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', back_populates='photos')
    comments = db.relationship('Comment', back_populates='photo', cascade='all')
    collectors = db.relationship('Collect', back_populates='collected', cascade='all')
    tags = db.relationship('Tag', secondary=tagging, back_populates='photos')


@whooshee.register_model('name')
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    photos = db.relationship('Photo', secondary=tagging, back_populates='tags')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    flag = db.Column(db.Integer, default=0)

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))

    photo = db.relationship('Photo', back_populates='comments')
    author = db.relationship('User', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    receiver = db.relationship('User', back_populates='notifications')


class Geometry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    axial_mode = db.Column(db.Integer)
    D1 = db.Column(db.Float)
    D2 = db.Column(db.Float)
    L = db.Column(db.Float)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', back_populates='geometries')
    experiments = db.relationship('Experiment', back_populates='geometry', cascade='all')

    def delete(self):
        default_geometry = Geometry.query.get(1)
        experiments = self.experiments[:]
        for experiment in experiments:
            experiment.geometry = default_geometry
        db.session.delete(self)
        db.session.commit()


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', back_populates='materials')
    experiments = db.relationship('Experiment', back_populates='material', cascade='all')

    def delete(self):
        default_material = Material.query.get(1)
        experiments = self.experiments[:]
        for experiment in experiments:
            experiment.material = default_material
        db.session.delete(self)
        db.session.commit()


class Extensometer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', back_populates='extensometers')
    experiments = db.relationship('Experiment', back_populates='extensometer', cascade='all')

    def delete(self):
        default_extensometer = Extensometer.query.get(1)
        experiments = self.experiments[:]
        for experiment in experiments:
            experiment.extensometer = default_extensometer
        db.session.delete(self)
        db.session.commit()


class Datafile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500))
    datafile_type = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_edit = db.Column(db.Boolean, default=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'))

    experiment = db.relationship('Experiment', back_populates='datafiles', cascade='all')


class Photofile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_edit = db.Column(db.Boolean, default=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'))

    experiment = db.relationship('Experiment', back_populates='photofiles', cascade='all')


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', back_populates='groups')

    experiments = db.relationship('Experiment', secondary=groups_experiments, back_populates='groups')  # collection

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True)
    exp_type = db.Column(db.Integer)
    temperature_max = db.Column(db.Float)
    temperature_range = db.Column(db.Float)
    axial_mode = db.Column(db.Integer)
    axial_ratio = db.Column(db.Float)
    axial_amplitude = db.Column(db.Float)
    torsional_mode = db.Column(db.Integer)
    torsional_ratio = db.Column(db.Float)
    torsional_amplitude = db.Column(db.Float)

    axial_torsional_phase = db.Column(db.Float)
    axial_temperature_phase = db.Column(db.Float)

    internal_cooling_air = db.Column(db.Float)
    life = db.Column(db.Integer)
    frequency = db.Column(db.Float)
    period = db.Column(db.Float)

    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_edit = db.Column(db.Boolean, default=True)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    geometry_id = db.Column(db.Integer, db.ForeignKey('geometry.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'))
    extensometer_id = db.Column(db.Integer, db.ForeignKey('extensometer.id'))

    author = db.relationship('User', back_populates='experiments')
    geometry = db.relationship('Geometry', back_populates='experiments')
    material = db.relationship('Material', back_populates='experiments')
    extensometer = db.relationship('Extensometer', back_populates='experiments')
    datafiles = db.relationship('Datafile', back_populates='experiment')
    photofiles = db.relationship('Photofile', back_populates='experiment')

    groups = db.relationship('Group', secondary=groups_experiments, back_populates='experiments')  # collection

    def delete(self):
        db.session.delete(self)
        db.session.commit()


@db.event.listens_for(User, 'after_delete', named=True)
def delete_avatars(**kwargs):
    target = kwargs['target']
    for filename in [target.avatar_s, target.avatar_m, target.avatar_l, target.avatar_raw]:
        if filename is not None:  # avatar_raw may be None
            path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], filename)
            if os.path.exists(path):  # not every filename map a unique file
                os.remove(path)


@db.event.listens_for(Photo, 'after_delete', named=True)
def delete_photos(**kwargs):
    target = kwargs['target']
    for filename in [target.filename, target.filename_s, target.filename_m]:
        path = os.path.join(current_app.config['MECHANICS_UPLOAD_PATH'], filename)
        if os.path.exists(path):  # not every filename map a unique file
            os.remove(path)


@db.event.listens_for(Datafile, 'after_delete', named=True)
def delete_datafiles(**kwargs):
    target = kwargs['target']
    for filename in [target.filename]:
        path = os.path.join(current_app.config['MECHANICS_UPLOAD_PATH'], filename)
        if os.path.exists(path):  # not every filename map a unique file
            os.remove(path)