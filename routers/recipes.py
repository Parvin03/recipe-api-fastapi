from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Recipe
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


@router.get("/")
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).all()


@router.post("/")
def create_recipe(recipe: RecipeCreate,
                  db: Session = Depends(get_db)):

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

@router.get("/{recipe_id}")
def get_recipe(recipe_id: int,
               db: Session = Depends(get_db)):

    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    if not recipe:
        return {"error": "Recipe not found"}

    return recipe

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