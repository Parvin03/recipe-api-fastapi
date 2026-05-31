from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import SessionLocal
from models import User, Recipe
from schemas import UserCreate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {"error": "User not found"}

    return user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {"error": "User not found"}

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


# User ranking by number of recipes
@router.get("/users-ranking")
def users_ranking(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            User.id,
            User.first_name,
            User.last_name,
            func.count(Recipe.id).label("recipes_count")
        )
        .outerjoin(Recipe, User.id == Recipe.user_id)
        .group_by(User.id)
        .order_by(func.count(Recipe.id).desc())
        .all()
    )

    return results