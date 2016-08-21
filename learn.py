from jsonschema import validate
from sklearn.ensemble import RandomForestClassifier

learn_schema = {
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


class Learn:
    @staticmethod
    def create_predictor(params):
        validate(params, learn_schema)
        data = params["data"]
        clf = RandomForestClassifier(n_estimators=10)
        fitted = clf.fit(data["inputs"], data["outputs"])
        return None
