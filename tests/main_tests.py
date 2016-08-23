import unittest
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
                '/learn',
                data=
                json.dumps(dict(
                    data=[
                        {
                            "inpuxts": [1, 2, 3],
                            "output": 5
                        }
                    ]
                )),
                content_type='application/json')
        self.assertTrue(isinstance(context.exception, ValidationError))

    def test_succeeds_on_correct_data(self):
        resp = self.app.post('/train', data=json.dumps(dict(
            data=[
                {
                    "inputs": [1, 2, 3],
                    "output": 5
                }
            ]
        )),
                             content_type='application/json')
        assert resp.status_code == 200


if __name__ == '__main__':
    unittest.main()
