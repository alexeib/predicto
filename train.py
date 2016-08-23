from jsonschema import validate

train_schema = {
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


class Train:
    @staticmethod
    def create_predictor(params):
        validate(params, train_schema)
        return None
