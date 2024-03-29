# -*- coding: utf-8 -*-
"""
    :author: Jingyu Sun
    :url: http://sunjingyu.com
    :copyright: © 2019 Jingyu Sun <sun.jingyu@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
import os
import random

from PIL import Image
from faker import Faker
from flask import current_app
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from mechanics.extensions import db
from mechanics.models import User, Photo, Tag, Comment, Notification
from mechanics.models import Material, Extensometer, Geometry, Experiment

from mechanics.python.Data import ExperimentLog


fake = Faker()
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def fake_admin():
    admin = User(name=u'管理员',
                 username='admin',
                 email='admin@admin.com',
                 # bio=fake.sentence(),
                 # website='http://sunjingyu.com',
                 confirmed=True,
                 role_id=4)
    admin.set_password('helloflask')
    notification = Notification(message='Hello, welcome to Mechanics.', receiver=admin)
    db.session.add(notification)
    db.session.add(admin)
    db.session.commit()


def fake_user(count=10):
    user = User(name=u'孙经雨',
                confirmed=True,
                username='sunjingyu',
                # bio=fake.sentence(),
                # location=fake.city(),
                # website=fake.url(),
                member_since=fake.date_this_decade(),
                email='sunwhale@126.com')
    user.set_password('123456')
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

    for name in [u'袁荒', u'杨俊杰', u'曾武', u'刘晖', u'杨正茂', u'杨茜茜', u'杨顺', u'庞科技', u'裴长浩', u'郭凯文', u'罗诚', u'张廷连', u'刘钰锦']:
        user = User(name=name,
                    confirmed=True,
                    username=fake.user_name(),
                    # bio=fake.sentence(),
                    # location=fake.city(),
                    # website=fake.url(),
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
    ExperimentLogFile = os.path.join(basedir, 'mechanics/python/Inconel718_test_log.csv')
    experiment_log = ExperimentLog(ExperimentLogFile)
    for name in experiment_log.number:
        regular = r'.*'
        load_type = experiment_log.obtainItem(name, 'load_type', regular)[0]
        comments = experiment_log.obtainItem(name, 'comments', regular)[0]
        test_date = experiment_log.obtainItem(name, 'test_date', regular)[0]
        regular = r'\d+\.?\d*'
        temperature_mode = experiment_log.obtainItem(name, 'temperature_mode', regular)
        if len(temperature_mode) == 1:
            temperature_max = float(temperature_mode[0])
            temperature_range = 0.0
        if len(temperature_mode) == 2:
            temperature_max = max(float(temperature_mode[0]), float(temperature_mode[1]))
            temperature_range = abs(float(temperature_mode[0]) - float(temperature_mode[1]))
        d_out = float(experiment_log.obtainItem(name, 'd_out', regular)[0])
        gauge_length = float(experiment_log.obtainItem(name, 'gauge_length', regular)[0])
        axial_strain = float(experiment_log.obtainItem(name, 'axial_strain', regular)[0])
        angel_strain = float(experiment_log.obtainItem(name, 'angel_strain', regular)[0])
        equivalent_strain = float(experiment_log.obtainItem(name, 'equivalent_strain', regular)[0])
        period = float(experiment_log.obtainItem(name, 'period', regular)[0])
        axial_temperature_phase = float(experiment_log.obtainItem(name, 'axial_temperature_phase', regular)[0])
        axial_rotational_phase = float(experiment_log.obtainItem(name, 'axial_rotational_phase', regular)[0])
        if period != 0:
            frequency = 1/period
        else:
            frequency = 0.0
        experiment = Experiment(name=name,
                                author=User.query.get(2),
                                material=Material.query.get(3),
                                exp_type=1,
                                extensometer=Extensometer.query.get(1),
                                geometry=Geometry.query.get(1),
                                timestamp=datetime.strptime(test_date, '%Y-%m-%d'),
                                temperature_max=temperature_max,
                                temperature_range=temperature_range,
                                axial_mode=2,
                                axial_ratio=-1.0,
                                axial_amplitude=axial_strain,
                                torsional_mode=2,
                                torsional_ratio=-1.0,
                                torsional_amplitude=angel_strain,
                                axial_torsional_phase=axial_rotational_phase,
                                axial_temperature_phase=axial_temperature_phase,
                                internal_cooling_air=random.randint(1, 100),
                                life=random.randint(100, 100000),
                                frequency=frequency,
                                period=period,
                                body=comments)
    # for i in range(count):
    #     experiment = Experiment(name=random.randint(1000, 9999),
    #                             author=User.query.get(random.randint(1, User.query.count())),
    #                             material=Material.query.get(random.randint(1, Material.query.count())),
    #                             exp_type=random.randint(1, 4),
    #                             extensometer=Extensometer.query.get(random.randint(1, Extensometer.query.count())),
    #                             geometry=Geometry.query.get(random.randint(1, Geometry.query.count())),
    #                             timestamp=fake.date_time_this_year(),
    #                             temperature_max=random.randint(20, 500),
    #                             temperature_range=random.randint(0, 500),
    #                             axial_mode=random.randint(1, 3),
    #                             axial_ratio=random.randint(-1, 1),
    #                             axial_amplitude = random.randint(0, 10),
    #                             torsional_mode = random.randint(1, 3),
    #                             torsional_ratio = random.randint(-1, 1),
    #                             torsional_amplitude = random.randint(0, 10),
    #                             axial_torsional_phase = random.randint(1, 180),
    #                             axial_temperature_phase = random.randint(1, 180),
    #                             internal_cooling_air = random.randint(1, 100),
    #                             life = random.randint(100, 100000),
    #                             frequency = random.randint(1, 10),
    #                             period = random.randint(1, 240),
    #                             body=fake.sentence())
        db.session.add(experiment)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()