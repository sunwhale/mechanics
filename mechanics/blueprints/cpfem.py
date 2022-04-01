# -*- coding: utf-8 -*-
"""
    :author: Jingyu Sun
    :url: http://sunjingyu.com
    :copyright: © 2019 Jingyu Sun <sun.jingyu@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response, \
    jsonify, send_from_directory, session
from flask_login import login_required, current_user

# from mechanics.emails import send_new_comment_email, send_new_reply_email
from mechanics.extensions import db
from mechanics.decorators import admin_required, permission_required
from mechanics.forms.data import ExperimentForm
from mechanics.models import Experiment, Geometry, User, Extensometer, Material, Datafile, Photofile, Group
from mechanics.utils import redirect_back


cpfem_bp = Blueprint('cpfem', __name__)


@cpfem_bp.route('/manage')
@login_required
def manage_cpfem():
    return render_template('cpfem/manage.html')


@cpfem_bp.route('/material/manage')
@login_required
def manage_material():
    return render_template('cpfem/manage_material.html')


# @data_bp.route('/material/new', methods=['GET', 'POST'])
# @login_required
# def new_material():
#     form = CreateMaterialForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         material = Material(name=name)
#         db.session.add(material)
#         db.session.commit()
#         flash('Material created.', 'success')
#         return redirect(url_for('.manage_material'))
#     return render_template('data/edit_material.html', form=form)


# @data_bp.route('/data', methods=['GET'])
# @login_required
# def get_data():
#     experiments = Experiment.query.all()
#     # experiments = Experiment.query.order_by(Experiment.id.desc()).all()
#     data_list = []
#     exp_type_list = ['Fatigue', 'Fracture', 'Monotonic', 'other']
#     for experiment in experiments:
#         data_list.append({"1": str(experiment.name),
#                           "2": experiment.author.name,
#                           "3": str(experiment.material.name),
#                           "4": exp_type_list[experiment.exp_type - 1],
#                           "5": str(experiment.timestamp.date()),
#                           "6": experiment.id})

#     data = {
#         "data": data_list
#     }
#     # print(data)
#     return jsonify(data)


# @data_bp.route('/data/user', methods=['GET'])
# @login_required
# def get_data_user():
#     user = current_user
#     experiments = Experiment.query.with_parent(user)
#     data_list = []
#     exp_type_list = ['Fatigue', 'Fracture', 'Monotonic', 'other']
#     for experiment in experiments:
#         data_list.append({"1": experiment.name,
#                           "2": experiment.author.name,
#                           "3": experiment.material.name,
#                           "4": exp_type_list[experiment.exp_type - 1],
#                           "5": str(experiment.timestamp.date()),
#                           "6": experiment.id})

#     data = {
#         "data": data_list
#     }
#     # print(data)
#     return jsonify(data)


# @data_bp.route('/data/group/<int:group_id>', methods=['GET'])
# @login_required
# def get_data_group(group_id):
#     user = current_user
#     group = Group.query.get_or_404(group_id)
#     experiments = Experiment.query.with_parent(group)
#     data_list = []
#     exp_type_list = ['Fatigue', 'Fracture', 'Monotonic', 'other']
#     for experiment in experiments:
#         data_list.append({"1": experiment.name,
#                           "2": experiment.author.name,
#                           "3": experiment.material.name,
#                           "4": exp_type_list[experiment.exp_type - 1],
#                           "5": str(experiment.timestamp.date()),
#                           "6": experiment.id})

#     data = {
#         "data": data_list
#     }
#     # print(data)
#     return jsonify(data)


# @data_bp.route('/datafile', methods=['GET'])
# @login_required
# def get_data_datafile():
#     datafiles = Datafile.query.order_by(Datafile.experiment_id).all()
#     data_list = []
#     datafile_type_list = [u'第一周（时域）', u'半寿命周（时域）', u'全时域', u'峰谷值', u'其他']
#     for datafile in datafiles:
#         data_list.append({"1": str(datafile.filename),
#                           "2": str(datafile.experiment.name),
#                           "3": str(round(datafile.size / 1024, 2)) + 'KB',
#                           "4": datafile_type_list[datafile.datafile_type - 1],
#                           "5": str(datafile.timestamp.date()),
#                           "6": [datafile.experiment_id, datafile.id]})

#     data = {
#         "data": data_list
#     }
#     # print(data)
#     return jsonify(data)