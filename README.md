# Recipe API

## Project Description

Recipe API is a backend application built with FastAPI, SQLAlchemy, SQLite, and Streamlit.

The application allows users to create recipes, rate recipes, search and filter recipes, upload recipe images, and view recipe rankings.

---

## Technologies

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Streamlit

---

## Features

### Users

* Create user
* Get all users
* Get user by ID
* Delete user

### Recipes

* Create recipe
* Get all recipes
* Get recipe by ID
* Update recipe
* Delete recipe

### Ratings

* Add rating
* Add comments
* Update rating
* Delete rating

### Search and Filtering

* Search by title
* Search by ingredients
* Search by category
* Filter by category
* Filter by difficulty

### Additional Features

* Top rated recipes
* Users ranking
* Image upload
* Streamlit frontend

---

## Run FastAPI

uvicorn main:app --reload

Swagger documentation:

http://127.0.0.1:8000/docs

---

## Run Streamlit

streamlit run streamlit_app.py
