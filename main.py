from flask import Flask, request
from learn import Learn

app = Flask(__name__)


@app.route('/learn', methods=['POST'])
def learn():
    params = request.get_json(force=False, silent=False, cache=False)
    Learn.create_predictor(params)
    return "Learned model"

if __name__ == "__main__":
    app.run()
