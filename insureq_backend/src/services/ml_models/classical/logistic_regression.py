# src/services/ml_models/logistic_regression.py
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


class LogisticRegressionModel:
    def __init__(self):
        self.model = LogisticRegression(solver="lbfgs", max_iter=200)

    def train(self, X_train, y_train):
        """
        Train the logistic regression model on the training data.
        """
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on test data and return performance metrics.
        """
        predictions = self.model.predict(X_test)

        return {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, average="weighted"),
            "recall": recall_score(y_test, predictions, average="weighted"),
            "f1_score": f1_score(y_test, predictions, average="weighted"),
        }
