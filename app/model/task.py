from app.model.base import Task as _Task, db


class Task(_Task):
    __table_args__ = {"useexisting": True}
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False, server_default=db.FetchedValue())
    project = db.relationship('app.model.project.Project')

    @property
    def project_name(self):
        return self.project.name if self.project else None
