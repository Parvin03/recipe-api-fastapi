from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import SessionLocal
from models import Recipe, Rating
from schemas import RecipeCreate

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Get all recipes with pagination
@router.get("/")
def get_recipes(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return (
        db.query(Recipe)
        .offset(skip)
        .limit(limit)
        .all()
    )

# Create recipe
@router.post("/")
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db)
):
    new_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        category=recipe.category,
        difficulty=recipe.difficulty,
        photo=recipe.photo,
        user_id=recipe.user_id
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe


# Get one recipe
@router.get("/{recipe_id}")
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    if not recipe:
        return {"error": "Recipe not found"}

    return recipe


# Update recipe
@router.put("/{recipe_id}")
def update_recipe(
    recipe_id: int,
    recipe_data: RecipeCreate,
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    if not recipe:
        return {"error": "Recipe not found"}

    recipe.title = recipe_data.title
    recipe.description = recipe_data.description
    recipe.ingredients = recipe_data.ingredients
    recipe.instructions = recipe_data.instructions
    recipe.category = recipe_data.category
    recipe.difficulty = recipe_data.difficulty
    recipe.photo = recipe_data.photo
    recipe.user_id = recipe_data.user_id

    db.commit()
    db.refresh(recipe)

    return recipe


# Delete recipe
@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    if not recipe:
        return {"error": "Recipe not found"}

    db.delete(recipe)
    db.commit()

    return {"message": "Recipe deleted successfully"}


# Search recipes
@router.get("/search/")
def search_recipes(
    title: str = None,
    ingredients: str = None,
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Recipe)

    if title:
        query = query.filter(
            Recipe.title.contains(title)
        )

    if ingredients:
        query = query.filter(
            Recipe.ingredients.contains(ingredients)
        )

    if category:
        query = query.filter(
            Recipe.category.contains(category)
        )

    return query.all()


# Filter recipes
@router.get("/filter/")
def filter_recipes(
    category: str = None,
    difficulty: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Recipe)

    if category:
        query = query.filter(
            Recipe.category == category
        )

    if difficulty:
        query = query.filter(
            Recipe.difficulty == difficulty
        )

    return query.all()


# Top rated recipes
@router.get("/top-rated/")
def get_top_rated_recipes(
    db: Session = Depends(get_db)
):
    recipes = db.query(Recipe).all()

    result = []

    for recipe in recipes:
        ratings = db.query(Rating).filter(
            Rating.recipe_id == recipe.id
        ).all()

        if ratings:
            avg_rating = sum(
                rating.value for rating in ratings
            ) / len(ratings)
        else:
            avg_rating = 0

        result.append({
            "id": recipe.id,
            "title": recipe.title,
            "average_rating": avg_rating
        })

    result.sort(
        key=lambda x: x["average_rating"],
        reverse=True
    )

    return result