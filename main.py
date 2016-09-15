from flask import Flask, request, abort, jsonify
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
    model_id = persistor.save(predictor)
    return model_id


@app.route('/predict/<string:model_id>', methods=['POST'])
def predict(model_id):
    params = request.get_json(force=False, silent=False, cache=False)
    if not isinstance(params, list):
        abort(500, 'Post data must be an array of inputs')
    persistor = model_persistor()
    model = persistor.load(model_id)
    if model is None:
        abort(404)
    probs = model.predict_proba(params)
    print(probs)
    return jsonify(probs.tolist())

if __name__ == "__main__":
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    app.run()
