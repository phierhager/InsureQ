# Example model in /models/model_performance.py
from sqlalchemy import Column, Integer, String, Numeric
from .database import Base


class ModelPerformance(Base):
    __tablename__ = "model_performances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    accuracy = Column(Numeric(precision=5, scale=2))
    precision = Column(Numeric(precision=5, scale=2))
    recall = Column(Numeric(precision=5, scale=2))
    f1_score = Column(Numeric(precision=5, scale=2))
