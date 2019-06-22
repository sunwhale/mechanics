# -*- coding: utf-8 -*-
"""
    :author: Jingyu Sun
    :url: http://sunjingyu.com
    :copyright: © 2019 Jingyu Sun <sun.jingyu@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField, IntegerField, FloatField, MultipleFileField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, NumberRange, ValidationError

from mechanics.models import User, Geometry, Extensometer, Experiment, Material, Datafile


class ExperimentForm(FlaskForm):
    name = IntegerField('Name')
    # author = SelectField('Author', coerce=int, default=1)
    exp_type = SelectField('Experiment type', coerce=int, default=1)
    material = SelectField('Material', coerce=int, default=1)
    geometry = SelectField('Geometry', coerce=int, default=1)
    extensometer = SelectField('Extensometer', coerce=int, default=1)
    temperature_max = FloatField(u'Temperature maximum, ℃', default=20)
    temperature_range = FloatField(u'Temperature range, ℃', default=0)
    axial_mode = SelectField('Axial control mode', coerce=int, default=1)
    axial_ratio = FloatField('Axial ratio', default=0)
    axial_amplitude = FloatField('Axial amplitude', default=0)
    torsional_mode = SelectField('Torsional control mode', coerce=int, default=1)
    torsional_ratio = FloatField('Torsional ratio', default=0)
    torsional_amplitude = FloatField('Torsional amplitude', default=0)
    axial_torsional_phase = FloatField('Axial torsional phase, deg', default=0)
    axial_temperature_phase = FloatField('Axial temperature phase, deg', default=0)
    internal_cooling_air = FloatField('Internal cooling air, l/min', default=0)
    life = IntegerField('Lifetime, cycle', default=1)
    frequency = FloatField('Frequency, Hz', default=1)
    period = FloatField('Period, s', default=1)
    body = CKEditorField('Comments')
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(ExperimentForm, self).__init__(*args, **kwargs)
        # self.author.choices = [(author.id, author.name)
        #                        for author in User.query.order_by(User.name).all()]
        self.extensometer.choices = [(extensometer.id, extensometer.name)
                                     for extensometer in Extensometer.query.order_by(Extensometer.name).all()]
        self.geometry.choices = [(geometry.id, geometry.name)
                                 for geometry in Geometry.query.order_by(Geometry.name).all()]
        self.material.choices = [(material.id, material.name)
                                 for material in Material.query.order_by(Material.name).all()]
        self.axial_mode.choices = [(1, 'displacement, mm'), (2, 'axial strain, mm/mm'), (3, 'force, kN'), (4, 'other')]
        self.torsional_mode.choices = [(1, 'rotation, deg'), (2, 'angle strain, deg'), (3, 'torque, N*m'), (4, 'other') ]
        self.exp_type.choices = [(1, 'Fatigue'), (2, 'Fracture'), (3, 'Monotonic'), (4, 'other') ]


class CreateExperimentForm(ExperimentForm):
    def validate_name(self, field):
        if Experiment.query.filter_by(name=field.data).first():
            raise ValidationError('The name is already in use.')


class EditExperimentForm(ExperimentForm):
    def __init__(self, experiment, *args, **kwargs):
        super(EditExperimentForm, self).__init__(*args, **kwargs)
        self.experiment = experiment

    def validate_name(self, field):
        if field.data != self.experiment.name and Experiment.query.filter_by(name=field.data).first():
            raise ValidationError('The name is already in use.')


class GeometryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    axial_mode = SelectField('Axial mode', coerce=int, default=1)
    D1 = FloatField('D1/D/W, mm', default=1)
    D2 = FloatField('D2/B, mm', default=1)
    L = FloatField('L, mm', default=1)
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(GeometryForm, self).__init__(*args, **kwargs)
        self.axial_mode.choices = [(1, u'#1 空心圆管 Tubular'), (2, u'#2 实心圆棒 Round'), (3, u'#3 板材 Plate')]


class CreateGeometryForm(GeometryForm):
    def validate_name(self, field):
        if Geometry.query.filter_by(name=field.data).first():
            raise ValidationError('The name is already in use.')


class EditGeometryForm(GeometryForm):
    def __init__(self, geometry, *args, **kwargs):
        super(EditGeometryForm, self).__init__(*args, **kwargs)
        self.geometry = geometry

    def validate_name(self, field):
        if field.data != self.geometry.name and Geometry.query.filter_by(name=field.data).first():
            raise ValidationError('The name is already in use.')


class ExtensometerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField(u'提交')


class CreateExtensometerForm(ExtensometerForm):
    def validate_name(self, field):
        if Extensometer.query.filter_by(name=field.data).first():
            raise ValidationError('The name is already in use.')


class EditExtensometerForm(ExtensometerForm):
    def __init__(self, extensometer, *args, **kwargs):
        super(EditExtensometerForm, self).__init__(*args, **kwargs)
        self.extensometer = extensometer

    def validate_name(self, field):
        if field.data != self.extensometer.name and Extensometer.query.filter_by(name=field.data).first():
            raise ValidationError('The name is already in use.')


class MaterialForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField(u'提交')


class CreateMaterialForm(MaterialForm):
    def validate_name(self, field):
        if Material.query.filter_by(name=field.data).first():
            raise ValidationError('The name is already in use.')


class EditMaterialForm(MaterialForm):
    def __init__(self, material, *args, **kwargs):
        super(EditMaterialForm, self).__init__(*args, **kwargs)
        self.material = material

    def validate_name(self, field):
        if field.data != self.material.name and Material.query.filter_by(name=field.data).first():
            raise ValidationError('The name is already in use.')


class DatafileForm(FlaskForm):
    filename = FileField(u'上传文件', validators=[FileRequired(), FileAllowed(['csv'])])
    datafile_type = SelectField(u'数据类型', coerce=int, default=1)
    description = TextAreaField(u'文件说明')
    submit = SubmitField(u'提交')
    def __init__(self, *args, **kwargs):
        super(DatafileForm, self).__init__(*args, **kwargs)
        self.datafile_type.choices = [(1, u'第一周（时域）'), (2, u'半寿命周（时域）'), (3, u'单调拉伸'), (4, u'峰谷值'), (5, u'其他') ]


class CreateDatafileForm(DatafileForm):
    def validate_name(self, field):
        if Datafile.query.filter_by(filename=field.data).first():
            raise ValidationError('The filename is already in use.')


class EditDatafileForm(DatafileForm):
    def __init__(self, datafile, *args, **kwargs):
        super(EditDatafileForm, self).__init__(*args, **kwargs)
        self.datafile = datafile

    def validate_name(self, field):
        if field.data != self.datafile.filename and Datafile.query.filter_by(filename=field.data).first():
            raise ValidationError('The filename is already in use.')