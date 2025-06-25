from pydantic import BaseModel, Field
from typing import Optional, List

class CatBase(BaseModel):
    name: str
    years_of_experience: int = Field(..., ge=0)
    breed: str
    salary: float = Field(..., ge=0)

class CatCreate(CatBase):
    pass

class CatUpdate(BaseModel):
    salary: float = Field(..., ge=0)

class Cat(CatBase):
    id: int

    class Config:
        from_attributes = True


class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""
    completed: Optional[bool] = False

class TargetCreate(TargetBase):
    pass

class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    completed: Optional[bool] = None

class Target(TargetBase):
    id: int

    class Config:
        from_attributes = True


class MissionBase(BaseModel):
    completed: Optional[bool] = False

class MissionCreate(MissionBase):
    cat_id: Optional[int] = None
    targets: List[TargetCreate] = Field(..., min_items=1, max_items=3)

class MissionUpdate(BaseModel):
    completed: Optional[bool]

class Mission(MissionBase):
    id: int
    cat_id: Optional[int]
    targets: List[Target]

    class Config:
        from_attributes = True
