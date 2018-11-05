# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Machine(db.Model):
    __tablename__ = 'machine'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    ip = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    user = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    password = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    hardware = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class Monitor(db.Model):
    __tablename__ = 'monitor'

    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, nullable=False, index=True)
    cpu = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    memory = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    disk = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    net = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    repository = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    machine_ids = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    directory = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    save_directory = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    pre_deploy = db.Column(db.Text)
    post_release = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    branch = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class Token(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), nullable=False, unique=True)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, index=True, server_default=db.FetchedValue())
    password = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
