import json

from app.model.base import Project as _Project
from app.model.machine import Machine


class Project(_Project):

    def get_machines(self):
        ids = json.loads(self.machine_ids)
        return Machine.query.filter(Machine.id.in_(ids)).all()

    @property
    def machine_names(self):
        return ','.join([m.name for m in self.get_machines()])
