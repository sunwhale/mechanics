# -*- coding: utf-8 -*-
"""
    :author: Jingyu Sun
    :url: http://greyli.com
    :copyright: © 2019 Jingyu Sun <sun.jingyu@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
import os
import random

from PIL import Image
from faker import Faker
from flask import current_app
from sqlalchemy.exc import IntegrityError

from mechanics.extensions import db
from mechanics.models import User, Photo, Tag, Comment, Notification
from mechanics.models import Material, Extensometer, Geometry, Experiment


fake = Faker()


def fake_admin():
    admin = User(name=u'孙经雨',
                 username='sunwhale',
                 email='sunwhale@126.com',
                 bio=fake.sentence(),
                 website='http://sunjingyu.com',
                 confirmed=True,
                 role_id=2)
    admin.set_password('helloflask')
    notification = Notification(message='Hello, welcome to Mechanics.', receiver=admin)
    db.session.add(notification)
    db.session.add(admin)
    db.session.commit()


def fake_user(count=10):
    for name in [u'袁荒', u'杨俊杰', u'曾武', u'刘晖', u'杨正茂', u'杨茜茜', u'杨顺', u'庞科技', u'裴长浩']:
        user = User(name=name,
                    confirmed=True,
                    username=fake.user_name(),
                    bio=fake.sentence(),
                    location=fake.city(),
                    website=fake.url(),
                    member_since=fake.date_this_decade(),
                    email=fake.email())
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_follow(count=30):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.follow(User.query.get(random.randint(1, User.query.count())))
    db.session.commit()


def fake_tag(count=20):
    for i in range(count):
        tag = Tag(name=fake.word())
        db.session.add(tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_photo(count=30):
    # photos
    upload_path = current_app.config['MECHANICS_UPLOAD_PATH']
    for i in range(count):
        print(i)

        filename = 'random_%d.jpg' % i
        r = lambda: random.randint(128, 255)
        img = Image.new(mode='RGB', size=(800, 800), color=(r(), r(), r()))
        img.save(os.path.join(upload_path, filename))

        photo = Photo(
            description=fake.text(),
            filename=filename,
            filename_m=filename,
            filename_s=filename,
            author=User.query.get(random.randint(1, User.query.count())),
            timestamp=fake.date_time_this_year()
        )

        # tags
        for j in range(random.randint(1, 5)):
            tag = Tag.query.get(random.randint(1, Tag.query.count()))
            if tag not in photo.tags:
                photo.tags.append(tag)

        db.session.add(photo)
    db.session.commit()


def fake_collect(count=50):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.collect(Photo.query.get(random.randint(1, Photo.query.count())))
    db.session.commit()


def fake_comment(count=100):
    for i in range(count):
        comment = Comment(
            author=User.query.get(random.randint(1, User.query.count())),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            photo=Photo.query.get(random.randint(1, Photo.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_material(count=5):
    for name in ['None','SS304', 'IN718', 'DD6', 'GH4169']:
        material = Material(name=name)
        db.session.add(material)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_extensometer(count=5):
    for name in ['None','uniaxial RT', 'baxial RT', 'epsilon', 'DIC']:
        extensometer = Extensometer(name=name)
        db.session.add(extensometer)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_geometry(count=5):
    for name in ['None', 'Solid', 'Tubular']:
        geometry = Geometry(name=name)
        db.session.add(geometry)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_experiment(count=100):
    for i in range(count):
        experiment = Experiment(name=random.randint(1000, 9999),
                                author=User.query.get(random.randint(1, User.query.count())),
                                material=Material.query.get(random.randint(1, Material.query.count())),
                                exp_type=random.randint(1, 4),
                                extensometer=Extensometer.query.get(random.randint(1, Extensometer.query.count())),
                                geometry=Geometry.query.get(random.randint(1, Geometry.query.count())),
                                timestamp=fake.date_time_this_year())
        db.session.add(experiment)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()