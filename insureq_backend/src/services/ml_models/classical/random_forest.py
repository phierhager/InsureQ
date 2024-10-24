from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


class RandomForestModel:
    def __init__(self):
        # Initialize a RandomForestClassifier with default settings
        self.model = RandomForestClassifier()

    def train(self, X_train, y_train):
        """
        Train the random forest model on the training data.
        """
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on test data and return performance metrics.
        """
        predictions = self.model.predict(X_test)
        probabilities = self.model.predict_proba(X_test)[:, 1]

        return {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(
                y_test, predictions, average="weighted"
            ),  # Use weighted for multiclass
            "recall": recall_score(y_test, predictions, average="weighted"),
            "f1_score": f1_score(y_test, predictions, average="weighted"),
        }
