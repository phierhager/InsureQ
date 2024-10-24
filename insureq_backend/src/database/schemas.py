from pydantic import BaseModel


class ModelPerformanceBase(BaseModel):
    name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float


class ModelPerformanceCreate(ModelPerformanceBase):
    pass


class ModelPerformanceSchema(ModelPerformanceBase):
    id: int

    class Config:
        from_attributes = True
