from sklearn.ensemble import RandomForestClassifier


class Trainer:
    @staticmethod
    def create_predictor(inputs, outputs):
        clf = RandomForestClassifier(n_estimators=10)
        fitted = clf.fit(inputs, outputs)
        return fitted
