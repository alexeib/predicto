from sklearn.externals import joblib
from uuid import uuid4
import os
import glob


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
        filename = self.make_path(name)
        for f in glob.glob(filename + '*'):
            os.remove(f)
