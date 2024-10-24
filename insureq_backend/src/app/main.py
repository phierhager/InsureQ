from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database.database import get_db, Base, engine, SessionLocal
from typing import List
from database.schemas import ModelPerformanceSchema
from services.model_services import get_model_performance, calculate_model_performances
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        yield
    finally:
        db.close()


@app.post("/api/performance/calculate", response_model=None)
def calculate_performance(db: Session = Depends(get_db)):
    try:
        calculate_model_performances(db=db)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Failed to calculate performance: {str(e)}"
        )


@app.get("/api/performance", response_model=List[ModelPerformanceSchema])
def get_performances(db: Session = Depends(get_db)):
    performances = get_model_performance(db=db)
    print([perf.name for perf in performances])
    return performances
