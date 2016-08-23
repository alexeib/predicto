from flask import Flask, request
import pickle
from train import Train

app = Flask(__name__)


@app.route('/train', methods=['POST'])
def train():
    params = request.get_json(force=False, silent=False, cache=False)
    predictor = Train.create_predictor(params)
    serialized = pickle.dumps(predictor)
    return serialized

if __name__ == "__main__":
    app.run()
