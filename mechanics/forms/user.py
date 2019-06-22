# -*- coding: utf-8 -*-
"""
    :author: Jingyu Sun
    :url: http://sunjingyu.com
    :copyright: © 2019 Jingyu Sun <sun.jingyu@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp

from mechanics.models import User


class EditProfileForm(FlaskForm):
    name = StringField(u'姓名', validators=[DataRequired(), Length(1, 30)])
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 20),
                                                   Regexp('^[a-zA-Z0-9]*$',
                                                          message='The username should contain only a-z, A-Z and 0-9.')])
    # website = StringField('Website', validators=[Optional(), Length(0, 255)])
    # location = StringField('City', validators=[Optional(), Length(0, 50)])
    # bio = TextAreaField('Bio', validators=[Optional(), Length(0, 120)])
    submit = SubmitField(u'提交')

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use.')


class UploadAvatarForm(FlaskForm):
    image = FileField(u'上传图片', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'The file format should be .jpg or .png.')
    ])
    submit = SubmitField(u'上传')


class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField(u'更新头像')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField(u'提交')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField(u'提交')


class NotificationSettingForm(FlaskForm):
    receive_comment_notification = BooleanField('New comment')
    receive_follow_notification = BooleanField('New follower')
    receive_collect_notification = BooleanField('New collector')
    submit = SubmitField(u'提交')


class PrivacySettingForm(FlaskForm):
    public_collections = BooleanField('Public my collection')
    submit = SubmitField(u'提交')


class DeleteAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField(u'提交')

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError('Wrong username.')
