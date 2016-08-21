from jsonschema import validate

learn_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Learning model creation schema",
    "type": "object",
    "properties": {
        "data": {
            "title": "Observations",
            "type": "array",
            "items": {
                "title": "Observation",
                "type": "object",
                "properties": {
                    "inputs": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    },
                    "output": {
                        "type": "number"
                    }
                },
                "required": ["inputs", "output"]
            }
        }
    },
    "required": ["data"]
}


class Learn:
    @staticmethod
    def create_predictor(params):
        print(params)
        validate(params, learn_schema)
        return None
