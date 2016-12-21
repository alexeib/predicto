import pytest
import main
from flask import json
from jsonschema import ValidationError


@pytest.fixture(scope='session')
def app():
    main.app.config['TESTING'] = True
    app = main.app.test_client(False)
    return app


def test_fails_on_wrong_data(app):
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


def test_succeeds_on_correct_data(mocker, app):
    rfc = mocker.patch('train.RandomForestClassifier')
    serialize_method = mocker.patch.object(main.FilePersistence, 'save', return_value='serialized')
    resp = app.post('/train', data=json.dumps(dict(
        data={
                "inputs": [[1, 2], [3, 4]],
                "outputs": [5, 1]
            }

    )), content_type='application/json')
    assert resp.status_code == 200
    assert resp.get_data() == b'serialized'
    assert serialize_method.called
    assert rfc.called
