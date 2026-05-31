import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🍲 Recipe Application")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "View Recipes",
        "Create Recipe",
        "Add Rating",
        "Top Rated Recipes",
        "Users Ranking"
    ]
)

# VIEW RECIPES
if menu == "View Recipes":
    st.header("Recipes")

    response = requests.get(f"{API_URL}/recipes/")

    if response.status_code == 200:
        recipes = response.json()

        for recipe in recipes:
            st.subheader(recipe["title"])
            st.write(f"Category: {recipe['category']}")
            st.write(f"Difficulty: {recipe['difficulty']}")
            st.write(recipe["description"])
            st.write("---")

# CREATE RECIPE
elif menu == "Create Recipe":
    st.header("Create Recipe")

    title = st.text_input("Title")
    description = st.text_area("Description")
    ingredients = st.text_area("Ingredients")
    instructions = st.text_area("Instructions")
    category = st.text_input("Category")
    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )
    user_id = st.number_input(
        "User ID",
        min_value=1,
        step=1
    )

    if st.button("Create Recipe"):

        data = {
            "title": title,
            "description": description,
            "ingredients": ingredients,
            "instructions": instructions,
            "category": category,
            "difficulty": difficulty,
            "photo": "",
            "user_id": user_id
        }

        response = requests.post(
            f"{API_URL}/recipes/",
            json=data
        )

        if response.status_code == 200:
            st.success("Recipe created!")

# ADD RATING
elif menu == "Add Rating":
    st.header("Add Rating")

    recipe_id = st.number_input(
        "Recipe ID",
        min_value=1,
        step=1
    )

    user_id = st.number_input(
        "User ID",
        min_value=1,
        step=1,
        key="user"
    )

    value = st.slider(
        "Rating",
        1,
        5
    )

    comment = st.text_area("Comment")

    if st.button("Submit Rating"):

        data = {
            "value": value,
            "comment": comment,
            "user_id": user_id,
            "recipe_id": recipe_id
        }

        response = requests.post(
            f"{API_URL}/ratings/",
            json=data
        )

        if response.status_code == 200:
            st.success("Rating added!")

# TOP RATED RECIPES
elif menu == "Top Rated Recipes":
    st.header("Top Rated Recipes")

    response = requests.get(
        f"{API_URL}/recipes/top-rated/"
    )

    if response.status_code == 200:
        recipes = response.json()

        for recipe in recipes:
            st.write(recipe)

# USERS RANKING
elif menu == "Users Ranking":
    st.header("Users Ranking")

    response = requests.get(
        f"{API_URL}/users-ranking"
    )

    if response.status_code == 200:
        users = response.json()

        for user in users:
            st.write(user)