from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class RecipeCreate(BaseModel):
    title: str
    description: str
    ingredients: str
    instructions: str
    category: str
    difficulty: str
    photo: Optional[str] = None
    user_id: int


class RecipeResponse(RecipeCreate):
    id: int

    class Config:
        from_attributes = True


class RatingCreate(BaseModel):
    value: int
    comment: str
    user_id: int
    recipe_id: int