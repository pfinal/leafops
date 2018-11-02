from flask import jsonify, request

from app.api import api
from app.model import to_dict
from app.model.base import  db
from app.model.project import Project


@api.route('/project')
def project():
    models = Project.query.order_by('id desc').all()

    return jsonify({'status': True, 'data': [to_dict(m, append_columns=['machine_names']) for m in models]})


@api.route('/project/create', methods=["POST"])
def project_create():
    project = Project()
    project.name = request.form['name']
    project.repository = request.form['repository']
    project.directory = request.form['directory']
    project.pre_deploy = request.form['pre_deploy']
    project.post_release = request.form['post_release']
    project.machine_ids = request.form['machine_ids']
    if project.machine_ids == "":
        project.machine_ids = "[]"

    db.session.add(project)
    db.session.commit()

    return jsonify({'status': True})


@api.route('/project/delete')
def project_delete():
    model = Project.query.get(request.args['id'])

    db.session.delete(model)
    db.session.commit()

    return jsonify({'status': True})
