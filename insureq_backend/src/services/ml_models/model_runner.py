# src/services/ml_models/model_runner.py
from .classical.logistic_regression import LogisticRegressionModel
from .classical.random_forest import RandomForestModel  # Assuming you add more models
from .base_model import BaseModel
from database.database import SessionLocal
from database.model_performance import ModelPerformance
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session
import logging
from . import model_registry


def run_evaluation(db: Session):
    try:
        # Load dataset
        iris = load_iris()
        X_train, X_test, y_train, y_test = train_test_split(
            iris.data, iris.target, test_size=0.2
        )

        for name, model in model_registry.items():
            existing_performance = (
                db.query(ModelPerformance).filter_by(name=name).first()
            )

            if not existing_performance:
                model.train(X_train, y_train)
                metrics = model.evaluate(X_test, y_test)

                performance = ModelPerformance(
                    name=name,
                    accuracy=metrics["accuracy"],
                    precision=metrics["precision"],
                    recall=metrics["recall"],
                    f1_score=metrics["f1_score"],
                )
                db.add(performance)
                db.commit()
                db.refresh(performance)

    except Exception as e:
        logging.error(f"Error in run_evaluation: {str(e)}")
        raise
