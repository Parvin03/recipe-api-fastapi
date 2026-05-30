from fastapi import FastAPI

from database import engine
from models import Base

from routers.users import router as users_router
from routers import recipes
from routers import ratings

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(recipes.router)
app.include_router(ratings.router)

@app.get("/")
def home():
    return {"message": "Recipe API is working"}