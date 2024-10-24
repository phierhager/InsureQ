from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database.model_performance import ModelPerformance
from database.database import engine, Base
from database.schemas import ModelPerformanceSchema, ModelPerformanceCreate
from database.database import get_db
from services.model_services import calculate_model_scores, get_model_performance
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/performance", response_model=List[ModelPerformanceSchema])
def read_model_performance(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    performances = get_model_performance(db=db, skip=skip, limit=limit)
    return performances


@app.post("/api/performance/calculate", response_model=ModelPerformanceSchema)
def calculate_performance(model_name: str, db: Session = Depends(get_db)):
    try:
        performance = calculate_model_scores(model_name=model_name, db=db)
        performances = db.query(ModelPerformance).all()
        return performances
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to calculate performance: {str(e)}"
        )


@app.get("/")
def read_root():
    return {"Hello": "World"}
