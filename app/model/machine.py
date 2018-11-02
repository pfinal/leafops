from app.model.base import Machine as _Machine
import json


class Machine(_Machine):

    @property
    def cpu(self):
        if self.hardware != '':
            temp = json.loads(self.hardware)
            return temp['cpu']

    @property
    def mem(self):
        if self.hardware != '':
            temp = json.loads(self.hardware)
            return temp['mem']
