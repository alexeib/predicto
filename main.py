from flask import Flask, request
from train import Train

app = Flask(__name__)


@app.route('/train', methods=['POST'])
def train():
    params = request.get_json(force=False, silent=False, cache=False)
    return Train.create_predictor(params)

if __name__ == "__main__":
    app.run()
