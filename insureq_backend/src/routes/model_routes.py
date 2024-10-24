from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.model_services import get_model_performance
from database.database import get_db

router = APIRouter()


@router.get("/models/performance")
def read_model_performance(db: Session = Depends(get_db)):
    return get_model_performance(db)
