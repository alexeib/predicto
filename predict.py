# from jsonschema import validate
# from sklearn.ensemble import RandomForestClassifier
#
# predict_schema = {
#     "$schema": "http://json-schema.org/draft-04/schema#",
#     "title": "Prediction schema",
#     "type": "object",
#     "properties": {
#         "modelType": {
#             "type": "string",
#             "title": "The type of serialized model. Allowed values: "
#         },
#         "data": {
#             "type": "object",
#             "title": "Training data",
#             "properties": {
#                 "inputs": {
#                     "title": "Array of inputs",
#                     "type": "array",
#                     "items": {
#                         "title": "Array of data for a single input",
#                         "type": "array",
#                         "items": {
#                             "type": "number",
#                         }
#                     }
#                 },
#                 "outputs": {
#                     "title": "Array of outputs",
#                     "type": "array",
#                     "items": {
#                         "type": "number"
#                     }
#                 }
#             },
#             "required": ["inputs", "outputs"]
#         }
#     },
#     "required": ["data"]
# }
#
#
# class Train:
#     @staticmethod
#     def create_predictor(params):
#         validate(params, train_schema)
#         data = params["data"]
#         clf = RandomForestClassifier(n_estimators=10)
#         fitted = clf.fit(data["inputs"], data["outputs"])
#         return fitted
