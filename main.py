from flask import Flask, request, abort, jsonify
from train import Trainer
from model_persistence import FilePersistence
from jsonschema import validate
import os


train_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Learning model creation schema",
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "title": "Training data",
            "properties": {
                "inputs": {
                    "title": "Array of inputs",
                    "type": "array",
                    "items": {
                        "title": "Array of data for a single input",
                        "type": "array",
                        "items": {
                            "type": "number",
                        }
                    }
                },
                "outputs": {
                    "title": "Array of outputs",
                    "type": "array",
                    "items": {
                        "type": "number"
                    }
                }
            },
            "required": ["inputs", "outputs"]
        }
    },
    "required": ["data"]
}


def make_app(persistor, trainer):
    app = Flask(__name__)

    @app.route('/train', methods=['POST'])
    def train():
        params = request.get_json(force=False, silent=False, cache=False)
        validate(params, train_schema)
        data = params["data"]
        predictor = trainer.create_predictor(data["inputs"], data["outputs"])
        model_id = persistor.save(predictor)
        return model_id

    @app.route('/predict/<string:model_id>', methods=['POST'])
    def predict(model_id):
        params = request.get_json(force=False, silent=False, cache=False)
        if not isinstance(params, list):
            abort(500, 'Post data must be an array of inputs')
        model = persistor.load(model_id)
        if model is None:
            abort(404)
        probs = model.predict_proba(params)
        return jsonify(probs.tolist())

    @app.route('/model/<string:model_id>', methods=['DELETE'])
    def delete(model_id):
        persistor.delete(model_id)
        return '', 204

    return app

if __name__ == "__main__":
    model_dir = './models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    app = make_app(FilePersistence(model_dir), Trainer())
    app.run()
