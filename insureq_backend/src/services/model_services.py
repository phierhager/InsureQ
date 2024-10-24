from sqlalchemy.orm import Session
from database.model_performance import ModelPerformance
from database.schemas import ModelPerformanceSchema, ModelPerformanceCreate
from services.ml_models.model_runner import run_evaluation
from sqlalchemy import func


def delete_duplicate_names(db: Session):
    # Step 1: Identify duplicates based on the 'name' field
    duplicates = (
        db.query(ModelPerformance.name, func.count(ModelPerformance.id))
        .group_by(ModelPerformance.name)
        .having(func.count(ModelPerformance.id) > 1)
        .all()
    )

    # Step 2: Delete all but one entry per duplicate name
    for name, count in duplicates:
        # Find all records with the duplicate name
        records = db.query(ModelPerformance).filter_by(name=name).all()

        # Keep the first record and delete the rest
        for record in records[1:]:
            db.delete(record)

    db.commit()


def get_model_performance(db: Session):
    delete_duplicate_names(db)
    performances = db.query(ModelPerformance).all()
    return [ModelPerformanceSchema.model_validate(perf) for perf in performances]


def calculate_model_performances(db: Session):
    run_evaluation(db)
