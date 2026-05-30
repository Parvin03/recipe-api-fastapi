from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Rating
from schemas import RatingCreate

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_ratings(db: Session = Depends(get_db)):
    return db.query(Rating).all()


@router.post("/")
def create_rating(
    rating: RatingCreate,
    db: Session = Depends(get_db)
):
    new_rating = Rating(
        value=rating.value,
        comment=rating.comment,
        user_id=rating.user_id,
        recipe_id=rating.recipe_id
    )

    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return new_rating


@router.get("/{rating_id}")
def get_rating(
    rating_id: int,
    db: Session = Depends(get_db)
):
    rating = db.query(Rating).filter(
        Rating.id == rating_id
    ).first()

    if not rating:
        return {"error": "Rating not found"}

    return rating


@router.put("/{rating_id}")
def update_rating(
    rating_id: int,
    rating_data: RatingCreate,
    db: Session = Depends(get_db)
):
    rating = db.query(Rating).filter(
        Rating.id == rating_id
    ).first()

    if not rating:
        return {"error": "Rating not found"}

    rating.value = rating_data.value
    rating.comment = rating_data.comment
    rating.user_id = rating_data.user_id
    rating.recipe_id = rating_data.recipe_id

    db.commit()
    db.refresh(rating)

    return rating


@router.delete("/{rating_id}")
def delete_rating(
    rating_id: int,
    db: Session = Depends(get_db)
):
    rating = db.query(Rating).filter(
        Rating.id == rating_id
    ).first()

    if not rating:
        return {"error": "Rating not found"}

    db.delete(rating)
    db.commit()

    return {"message": "Rating deleted successfully"}