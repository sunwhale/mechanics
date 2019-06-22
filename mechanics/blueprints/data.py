# -*- coding: utf-8 -*-
"""
    :author: Jingyu Sun
    :url: http://sunjingyu.com
    :copyright: © 2019 Jingyu Sun <sun.jingyu@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response, jsonify, send_from_directory, session
from flask_login import login_required, current_user

# from mechanics.emails import send_new_comment_email, send_new_reply_email
from mechanics.extensions import db
from mechanics.forms.data import ExperimentForm, CreateGeometryForm, EditGeometryForm, CreateExtensometerForm, \
    EditExtensometerForm, CreateExperimentForm, EditExperimentForm, EditMaterialForm, CreateMaterialForm, EditMaterialForm, \
    CreateDatafileForm, EditDatafileForm, DatafileForm
from mechanics.models import Experiment, Geometry, User, Extensometer, Material, Datafile
from mechanics.utils import redirect_back


data_bp = Blueprint('data', __name__)


@data_bp.route('/experiment/manage')
@login_required
def manage_experiment():
    return render_template('data/manage_experiment.html')


@data_bp.route('/experiment/new', methods=['GET', 'POST'])
@login_required
def new_experiment():
    form = CreateExperimentForm()
    if form.validate_on_submit():
        name = form.name.data
        # author = User.query.get(form.author.data)
        author = current_user
        exp_type = form.exp_type.data
        material = Material.query.get(form.material.data)
        geometry = Geometry.query.get(form.geometry.data)
        extensometer = Extensometer.query.get(form.extensometer.data)
        temperature_max = form.temperature_max.data
        temperature_range = form.temperature_range.data
        axial_mode = form.axial_mode.data
        axial_ratio = form.axial_ratio.data
        axial_amplitude = form.axial_amplitude.data
        torsional_mode = form.torsional_mode.data
        torsional_ratio = form.torsional_ratio.data
        torsional_amplitude = form.torsional_amplitude.data
        axial_torsional_phase = form.axial_torsional_phase.data
        axial_temperature_phase = form.axial_temperature_phase.data
        internal_cooling_air = form.internal_cooling_air.data
        life = form.life.data
        frequency = form.frequency.data
        period = form.period.data
        body = form.body.data

        experiment = Experiment(name=name,
                                author=author,
                                exp_type=exp_type,
                                material=material,
                                geometry=geometry,
                                extensometer=extensometer,
                                temperature_max=temperature_max,
                                temperature_range=temperature_range,
                                axial_mode=axial_mode,
                                axial_ratio=axial_ratio,
                                axial_amplitude=axial_amplitude,
                                torsional_mode=torsional_mode,
                                torsional_ratio=torsional_ratio,
                                torsional_amplitude=torsional_amplitude,
                                axial_torsional_phase=axial_torsional_phase,
                                axial_temperature_phase=axial_temperature_phase,
                                internal_cooling_air=internal_cooling_air,
                                life=life,
                                frequency=frequency,
                                period=period,
                                body=body)

        # same with:
        # geometry_id = form.geometry.data
        # post = Post(title=title, body=body, geometry_id=geometry_id)
        db.session.add(experiment)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('data.manage_experiment'))
    return render_template('data/edit_experiment.html', form=form)


@data_bp.route('/experiment/<int:experiment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_experiment(experiment_id):
    experiment = Experiment.query.get_or_404(experiment_id)
    form = EditExperimentForm(experiment=experiment)
    if current_user != experiment.author and not current_user.can('MODERATE'):
        flash(u'该试验录入人为：' + experiment.author.name + u'，您无法编辑，如需编辑请联系试验录入人或管理员。', 'warning')
        abort(403)
    if (datetime.utcnow() - experiment.timestamp).days > 30 or current_user.can('MODERATE'):
        flash(u'试验创建日期：' + str(experiment.timestamp) + u'，已经超出可编辑时间（30天），请联系管理员。', 'warning')
        abort(403)
    if form.validate_on_submit():
        experiment.name = form.name.data
        # experiment.author = User.query.get(form.author.data)
        experiment.exp_type = form.exp_type.data
        experiment.material = Material.query.get(form.material.data)
        experiment.geometry = Geometry.query.get(form.geometry.data)
        experiment.extensometer = Extensometer.query.get(form.extensometer.data)
        experiment.temperature_max = form.temperature_max.data
        experiment.temperature_range = form.temperature_range.data
        experiment.axial_mode = form.axial_mode.data
        experiment.axial_ratio = form.axial_ratio.data
        experiment.axial_amplitude = form.axial_amplitude.data
        experiment.torsional_mode = form.torsional_mode.data
        experiment.torsional_ratio = form.torsional_ratio.data
        experiment.torsional_amplitude = form.torsional_amplitude.data
        experiment.axial_torsional_phase = form.axial_torsional_phase.data
        experiment.axial_temperature_phase = form.axial_temperature_phase.data
        experiment.internal_cooling_air = form.internal_cooling_air.data
        experiment.life = form.life.data
        experiment.frequency = form.frequency.data
        experiment.period = form.period.data
        experiment.body = form.body.data
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('data.manage_experiment'))

    form.name.data = experiment.name
    # form.author.data = experiment.author_id
    form.exp_type.data = experiment.exp_type
    form.material.data = experiment.material_id
    form.geometry.data = experiment.geometry_id
    form.extensometer.data = experiment.extensometer_id
    form.temperature_max.data = experiment.temperature_max
    form.temperature_range.data = experiment.temperature_range
    form.axial_mode.data = experiment.axial_mode
    form.axial_ratio.data = experiment.axial_ratio
    form.axial_amplitude.data = experiment.axial_amplitude
    form.torsional_mode.data = experiment.torsional_mode
    form.torsional_ratio.data = experiment.torsional_ratio
    form.torsional_amplitude.data = experiment.torsional_amplitude
    form.axial_torsional_phase.data = experiment.axial_torsional_phase
    form.axial_temperature_phase.data = experiment.axial_temperature_phase
    form.internal_cooling_air.data = experiment.internal_cooling_air
    form.life.data = experiment.life
    form.frequency.data = experiment.frequency
    form.period.data = experiment.period
    form.body.data = experiment.body
    return render_template('data/edit_experiment.html', form=form)


@data_bp.route('/experiment/<int:experiment_id>/delete', methods=['POST'])
@login_required
def delete_experiment(experiment_id):
    experiment = Experiment.query.get_or_404(experiment_id)
    experiment.delete()
    flash('Experiment deleted.', 'success')
    return redirect(url_for('data.manage_experiment'))


@data_bp.route('/experiment/<int:experiment_id>/view', methods=['GET', 'POST'])
@login_required
def view_experiment(experiment_id):
    experiment = Experiment.query.get_or_404(experiment_id)
    return render_template('data/view_experiment.html', experiment=experiment)


@data_bp.route('/experiment/<int:experiment_id>/datafile', methods=['GET', 'POST'])
@login_required
def datafile_experiment(experiment_id):
    experiment = Experiment.query.get_or_404(experiment_id)
    author = experiment.author
    # datafiles = Datafile.query.with_parent(experiment).order_by(Datafile.filename.desc())

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MECHANICS_PHOTO_PER_PAGE']
    pagination = Datafile.query.with_parent(experiment).order_by(Datafile.filename.asc()).paginate(page, per_page)
    datafiles = pagination.items

    form = CreateDatafileForm()
    if form.validate_on_submit():
        f = form.filename.data
        description = form.description.data
        datafile_type = form.datafile_type.data
        experiment_id = experiment.id
        filename = str(experiment.name) + '_' + str(datafile_type) + '_' + '.csv'

        for d in datafiles:
            if d.filename == filename:
                flash(filename + u'文件已经存在，清删除相关文件再次上传。', 'danger')
                return redirect(url_for('data.datafile_experiment', experiment_id=experiment_id))

        datafile = Datafile(description=description,
                            filename=filename,
                            datafile_type=datafile_type,
                            experiment_id=experiment_id)

        f.save(os.path.join(current_app.config['MECHANICS_UPLOAD_PATH'], filename))
        # session['filenames'] = [filename]
        flash(u'上传成功。', 'success')
        db.session.add(datafile)
        db.session.commit()
        return redirect(url_for('data.datafile_experiment', experiment_id=experiment_id, datafiles=datafiles, author=author))
    return render_template('data/datafile_experiment.html', experiment=experiment, datafiles=datafiles, form=form, author=author)


# @data_bp.route('/datafile/<int:datafile_id>/edit', methods=['GET', 'POST'])
# @login_required
# def edit_datafile(datafile_id):
#     datafile = Datafile.query.get_or_404(datafile_id)
#     experiment_id = datafile.experiment_id
#     experiment = Experiment.query.get_or_404(experiment_id)
#     datafiles = Datafile.query.with_parent(experiment).order_by(Datafile.timestamp.desc())
#     form = CreateDatafileForm()
#     if form.validate_on_submit():
#         f = form.filename.data
#         filename = f.filename
#         description = form.description.data
#         datafile_type = form.datafile_type.data
#         experiment_id = experiment.id
#
#         for d in datafiles:
#             if d.filename == filename:
#                 flash(filename + u'文件已经存在，清删除相关文件再次上传。', 'danger')
#                 return redirect(url_for('data.datafile_experiment', experiment_id=experiment_id))
#
#         datafile = Datafile(description=description,
#                             filename=filename,
#                             datafile_type=datafile_type,
#                             experiment_id=experiment_id)
#
#         f.save(os.path.join(current_app.config['MECHANICS_UPLOAD_PATH'], filename))
#         # session['filenames'] = [filename]
#         flash(u'上传成功。', 'success')
#         db.session.add(datafile)
#         db.session.commit()
#         return redirect(url_for('data.datafile_experiment', experiment_id=experiment_id))
#     return render_template('data/datafile_experiment.html', experiment=experiment, datafiles=datafiles, form=form)


@data_bp.route('/datafile/<int:datafile_id>/delete', methods=['POST'])
@login_required
def delete_datafile(datafile_id):
    datafile = Datafile.query.get_or_404(datafile_id)
    experiment_id = datafile.experiment_id
    experiment = Experiment.query.get_or_404(experiment_id)

    if current_user != experiment.author and not current_user.can('MODERATE'):
        abort(403)

    experiment.datafiles.remove(datafile)
    db.session.commit()

    db.session.delete(datafile)
    db.session.commit()

    flash(datafile.filename + u'文件删除成功。', 'info')
    return redirect(url_for('data.datafile_experiment', experiment_id=experiment_id))


@data_bp.route('/geometry/manage')
@login_required
def manage_geometry():
    return render_template('data/manage_geometry.html')


@data_bp.route('/geometry/new', methods=['GET', 'POST'])
@login_required
def new_geometry():
    form = CreateGeometryForm()
    if form.validate_on_submit():
        name = form.name.data
        axial_mode = form.axial_mode.data
        D1 = form.D1.data
        D2 = form.D2.data
        L = form.L.data
        geometry = Geometry(name=name,
                            axial_mode=axial_mode,
                            D1=D1,
                            D2=D2,
                            L=L)
        db.session.add(geometry)
        db.session.commit()
        flash('Geometry created.', 'success')
        return redirect(url_for('.manage_geometry'))
    return render_template('data/edit_geometry.html', form=form)


@data_bp.route('/geometry/<int:geometry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_geometry(geometry_id):
    geometry = Geometry.query.get_or_404(geometry_id)
    form = EditGeometryForm(geometry=geometry)
    if geometry.id == 1:
        flash('You can not edit the default geometry.', 'warning')
        return redirect(url_for('.manage_geometry'))
    if form.validate_on_submit():
        geometry.name = form.name.data
        geometry.axial_mode = form.axial_mode.data
        geometry.D1 = form.D1.data
        geometry.D2 = form.D2.data
        geometry.L = form.L.data
        db.session.commit()
        flash('Geometry updated.', 'success')
        return redirect(url_for('.manage_geometry'))
    form.name.data = geometry.name
    form.axial_mode.data = geometry.axial_mode
    form.D1.data = geometry.D1
    form.D2.data = geometry.D2
    form.L.data = geometry.L
    return render_template('data/edit_geometry.html', form=form)


@data_bp.route('/geometry/<int:geometry_id>/delete', methods=['POST'])
@login_required
def delete_geometry(geometry_id):
    geometry = Geometry.query.get_or_404(geometry_id)
    if geometry.id == 1:
        flash('You can not delete the default geometry.', 'warning')
        return redirect(url_for('.manage_geometry'))
    geometry.delete()
    flash('Geometry deleted.', 'success')
    return redirect(url_for('.manage_geometry'))


@data_bp.route('/extensometer/manage')
@login_required
def manage_extensometer():
    return render_template('data/manage_extensometer.html')


@data_bp.route('/extensometer/new', methods=['GET', 'POST'])
@login_required
def new_extensometer():
    form = CreateExtensometerForm()
    if form.validate_on_submit():
        name = form.name.data
        extensometer = Extensometer(name=name)
        db.session.add(extensometer)
        db.session.commit()
        flash('Extensometer created.', 'success')
        return redirect(url_for('.manage_extensometer'))
    return render_template('data/edit_extensometer.html', form=form)


@data_bp.route('/extensometer/<int:extensometer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_extensometer(extensometer_id):
    extensometer = Extensometer.query.get_or_404(extensometer_id)
    form = EditExtensometerForm(extensometer=extensometer)
    if extensometer.id == 1:
        flash('You can not edit the default extensometer.', 'warning')
        return redirect(url_for('.manage_extensometer'))
    if form.validate_on_submit():
        extensometer.name = form.name.data
        db.session.commit()
        flash('Extensometer updated.', 'success')
        return redirect(url_for('.manage_extensometer'))
    form.name.data = extensometer.name
    return render_template('data/edit_extensometer.html', form=form)


@data_bp.route('/extensometer/<int:extensometer_id>/delete', methods=['POST'])
@login_required
def delete_extensometer(extensometer_id):
    extensometer = Extensometer.query.get_or_404(extensometer_id)
    if extensometer.id == 1:
        flash('You can not delete the default extensometer.', 'warning')
        return redirect(url_for('.manage_extensometer'))
    extensometer.delete()
    flash('Extensometer deleted.', 'success')
    return redirect(url_for('.manage_extensometer'))


@data_bp.route('/material/manage')
@login_required
def manage_material():
    return render_template('data/manage_material.html')


@data_bp.route('/material/new', methods=['GET', 'POST'])
@login_required
def new_material():
    form = CreateMaterialForm()
    if form.validate_on_submit():
        name = form.name.data
        material = Material(name=name)
        db.session.add(material)
        db.session.commit()
        flash('Material created.', 'success')
        return redirect(url_for('.manage_material'))
    return render_template('data/edit_material.html', form=form)


@data_bp.route('/material/<int:material_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_material(material_id):
    material = Material.query.get_or_404(material_id)
    form = EditMaterialForm(material=material)
    if material.id == 1:
        flash('You can not edit the default material.', 'warning')
        return redirect(url_for('.manage_material'))
    if form.validate_on_submit():
        material.name = form.name.data
        db.session.commit()
        flash('Material updated.', 'success')
        return redirect(url_for('.manage_material'))
    form.name.data = material.name
    return render_template('data/edit_material.html', form=form)


@data_bp.route('/material/<int:material_id>/delete', methods=['POST'])
@login_required
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    if material.id == 1:
        flash('You can not delete the default material.', 'warning')
        return redirect(url_for('.manage_material'))
    material.delete()
    flash('Material deleted.', 'success')
    return redirect(url_for('.manage_material'))


@data_bp.route('/data', methods=['GET'])
@login_required
def get_data():
    experiments = Experiment.query.all()
    data_list = []
    exp_type_list = ['Fatigue', 'Fracture', 'Monotonic', 'other']
    for experiment in experiments:
        data_list.append({ "1": experiment.name,
                           "2": experiment.author.name,
                           "3": experiment.material.name,
                           "4": exp_type_list[experiment.exp_type-1],
                           "5": str(experiment.timestamp),
                           "6": experiment.id })

    data = {
        "data": data_list
    }
    print data
    return jsonify(data)


@data_bp.route('/data/user', methods=['GET'])
@login_required
def get_data_user():
    user = current_user
    experiments = Experiment.query.with_parent(user)
    data_list = []
    exp_type_list = ['Fatigue', 'Fracture', 'Monotonic', 'other']
    for experiment in experiments:
        data_list.append({ "1": experiment.name,
                           "2": experiment.author.name,
                           "3": experiment.material.name,
                           "4": exp_type_list[experiment.exp_type-1],
                           "5": str(experiment.timestamp),
                           "6": experiment.id })

    data = {
        "data": data_list
    }
    print data
    return jsonify(data)


@data_bp.route('/uploads/<path:filename>')
@login_required
def get_datafile(filename):
    return send_from_directory(current_app.config['MECHANICS_UPLOAD_PATH'], filename)