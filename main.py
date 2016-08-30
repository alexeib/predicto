from flask import Flask, request
from train import Train
from model_persistence import FilePersistence
import os

app = Flask(__name__)
model_dir = './models'


def model_persistor():
    return FilePersistence(model_dir)


@app.route('/train', methods=['POST'])
def train():
    params = request.get_json(force=False, silent=False, cache=False)
    persistor = model_persistor()
    predictor = Train.create_predictor(params)
    serialized = persistor.save(predictor)
    return serialized

if __name__ == "__main__":
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    app.run()
