import unittest
from unittest.mock import patch
import main
from flask import json
from jsonschema import ValidationError


class PredictoTestCase(unittest.TestCase):
    def setUp(self):
        main.app.config['TESTING'] = True
        self.app = main.app.test_client(False)

    def test_fails_on_wrong_data(self):
        with self.assertRaises(Exception) as context:
            self.app.post(
                '/train',
                data=
                json.dumps(dict(
                    data={
                            "inpuxts": [1, 2, 3],
                            "output": 5
                    }
                )),
                content_type='application/json')
        self.assertTrue(isinstance(context.exception, ValidationError))

    @patch('train.RandomForestClassifier')
    def test_succeeds_on_correct_data(self, rfc):
        with patch.object(main.FilePersistence, 'save', return_value = 'serialized') as serialize_method:
            resp = self.app.post('/train', data=json.dumps(dict(
                data={
                        "inputs": [[1, 2], [3, 4]],
                        "outputs": [5, 1]
                    }

            )), content_type='application/json')
        assert resp.status_code == 200
        assert resp.get_data() == b'serialized'
        assert serialize_method.called
        assert rfc.called


if __name__ == '__main__':
    unittest.main()
