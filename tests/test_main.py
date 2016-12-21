from main import make_app
from train import Trainer
from model_persistence import MemoryPersistence
import pytest
from flask import json
from jsonschema import ValidationError


@pytest.fixture()
def persistence():
    return MemoryPersistence()

@pytest.fixture()
def trainer():
    return Trainer()

@pytest.fixture()
def app(persistence, trainer):
    app = make_app(persistence, trainer)
    app.config['TESTING'] = True
    app = app.test_client(False)
    return app


def train(app, inputs, outputs):
    return app.post('/train', data=json.dumps(dict(
        data={
            "inputs": inputs,
            "outputs": outputs
        }

    )), content_type='application/json')


def predict(app, model_name, inputs):
    return app.post('/predict/{}'.format(model_name.decode('utf-8')),
                    data=json.dumps(inputs),
                    content_type='application/json')

def test_train_fails_on_wrong_data(app):
    with pytest.raises(ValidationError):
        app.post(
            '/train',
            data=
            json.dumps(dict(
                data={
                        "inpuxts": [1, 2, 3],
                        "output": 5
                }
            )),
            content_type='application/json')


def test_train_succeeds_on_correct_data(mocker, app, persistence, trainer):
    create_predictor_method = mocker.patch.object(trainer, 'create_predictor')
    serialize_method = mocker.patch.object(persistence, 'save', return_value='serialized')
    resp = train(app, [[1, 2], [3, 4]], [5,1])
    assert resp.status_code == 200
    assert resp.get_data() == b'serialized'
    assert serialize_method.called
    assert create_predictor_method.called


def test_predict_correctly_predicts(app):
    resp = train(app, [[1, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 1, 0], [0, 0, 1]],
                      [ 0,         0,         0,         0,         1,         1,         1,         1])
    model_name = resp.get_data()
    predict_resp = predict(app, model_name, [[1, 1, 0], [0, 0, 1]])
    assert resp.status_code == 200
    predictions = json.loads(predict_resp.get_data())
    assert len(predictions) == 2
    assert len(predictions[0]) == 2
    assert len(predictions[1]) == 2
    assert predictions[0][0] > predictions[0][1]
    assert predictions[1][0] < predictions[1][1]
