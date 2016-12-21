from sklearn.externals import joblib
from uuid import uuid4
import os


class FilePersistence:
    def __init__(self, save_dir):
        self._save_dir = save_dir

    def make_path(self, name):
        path = os.path.join(self._save_dir, name + '.mdl')
        return path

    def save(self, model):
        name = str(uuid4())
        filename = self.make_path(name)
        joblib.dump(model, filename)
        return name

    def load(self, name):
        filename = self.make_path(name)
        return joblib.load(filename)

    def delete(self, name):
        if not name or (isinstance(name, str) and name.isspace()):
                raise ValueError('name must not be an empty')
        filename = self.make_path(name)
        os.remove(filename)


class MemoryPersistence:
    def __init__(self):
        self.models = {}

    def save(self, model):
        name = str(uuid4())
        self.models[name] = model
        return name

    def load(self, name):
        return self.models[name]

    def delete(self, name):
        del self.models[name]
