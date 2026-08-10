import streamlit as st
import csv
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

st.markdown('<h1 style="text-align: center; color: chocolate;">Welcome to the Recipe Recommender</h1>', unsafe_allow_html=True)
st.write("\n")
st.markdown(" ##### Write an ingredient you would like to use. Please be specific.")
st.write(" ###### Tip: Its recommended to use keywords like 'raw', 'cooked', 'fresh', 'frozen' or specific cuts like 'ground' or 'breast'.")
ingredients = st.text_input("")

st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: rgba(255, 140, 0, 0.3) !important;
        color: white !important;
        border: none;
        outline: none;
        border-radius: 4px;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: rgba(255, 140, 0, 0.9) !important;
        color: white !important;
        border-color: #FF8C00 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if ingredients:
    search_words = ingredients.lower().split()

    scored_results = []

    with open('food.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)

            next(reader)
        
            for row in reader:
                description = row[2].lower()
                
                score = 0

                for word in search_words:
                    if word in description:
                        score += 1
                
                if score > 0:
                    scored_results.append((score, description))
            scored_results.sort(reverse=True)

            st.write("\n")
            st.write(" ##### Top Results:")

            if 'selected' not in st.session_state:
                st.session_state.selected = {}

            for i in range(min(5, len(scored_results))):
                ingredient_name = scored_results[i][1]
                
                if st.button(f"Add {ingredient_name}"):
                    if ingredient_name not in st.session_state.selected:
                        st.session_state.selected[ingredient_name] = 0
                        st.rerun()

            st.write("\n")
            st.write(" ##### Selected Ingredients:")
            for item in list(st.session_state.selected.keys()):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"{item}")
                    
                with col2:
                    units = {}
                    with open('food.csv', mode='r', encoding='utf-8') as file1:
                        id_reader = csv.reader(file1)
                        
                        for row in id_reader:
                            description = row[2].lower()
                            if description == item.lower():
                                id = row[0]
                                break

                    with open('food_portion.csv', mode='r', encoding='utf-8') as file2:
                        portion_reader = csv.reader(file2)

                        for row in portion_reader:
                            if row[1] == id:
                                portion_amount = float(row[3])
                                unit_name = row[6]
                                total_grams = float(row[7])

                                if unit_name and portion_amount > 0:
                                    single_unit_weight = total_grams / portion_amount
                                    units[unit_name] = single_unit_weight

                    selected_unit = st.selectbox("Unit:", list(units.keys()), index=None, placeholder="Select unit...", key=f"unit_box_{item}")

                with col3:
                    current_amount = st.session_state.selected[item]
                    new_amount = st.number_input("Value:", min_value=0.0, value=float(current_amount), step=1.0, key=f"amount_{item}")

                    st.session_state.selected[item] = new_amount

                    if st.session_state.get(f"unit_box_{item}"):
                        active_unit = st.session_state[f"unit_box_{item}"]
                        gram_amount = new_amount * units.get(active_unit)
                        st.write(f"Amount in grams: {gram_amount:.2f}")
                        st.session_state.selected[item] = gram_amount
                      
                with col4:
                    if st.button("Remove", key=f"remove_{item}"):
                        del st.session_state.selected[item]
                        st.rerun()

st.write("\n")

find_recipes = False
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Find Recipes",type="primary", use_container_width=True):
        find_recipes = True
if find_recipes:
    cleaned_ingredients = {}
    for item in st.session_state.selected.keys():
        clean_ingredient = item.split(",")[0].strip().replace(" ", "+").lower()
        cleaned_ingredients[clean_ingredient] = st.session_state.selected.get(item)

    ingredient_string = ",".join(cleaned_ingredients.keys())

    recipe_url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient_string}&number=5&ranking=1&apiKey={API_KEY}"

    response = requests.get(recipe_url)
    data = response.json()

    valid_recipes = []

    for recipe in data:
        valid_recipe = True

        recipe_ingredients_url = f"https://api.spoonacular.com/recipes/{recipe["id"]}/information?includeNutrition=false&apiKey={API_KEY}"
        response2 = requests.get(recipe_ingredients_url)
        data2 = response2.json()

        for ingredient in data2["extendedIngredients"]:
            name = ingredient["name"].lower()

            measurements = ingredient["measures"]["metric"]

            amount = measurements["amount"]
            recipe_unit = measurements["unitLong"].lower()

            match = None
            for user_ingredient in st.session_state.selected.keys():
                if name in user_ingredient or user_ingredient in name:
                    match = True
                    description2 = user_ingredient
                    users_amount = st.session_state.selected.get(user_ingredient)
                    break

            final_grams = 0

            if match:
                with open('food_portion.csv', mode='r', encoding='utf-8') as file3, \
                    open('food.csv', mode='r', encoding='utf-8') as file4:
                    portion_reader1 = csv.reader(file3)
                    id_reader2 = csv.reader(file4)
                    next(portion_reader1)
                    next(id_reader2)
                    
                    for row in id_reader2:
                        description = row[2].lower()
                        if description == description2:
                            id = row[0]
                            break

                    unit_families = [
                        ["tbsp", "tbs", "tablespoon", "tablespoons"],
                        ["tsp", "teaspoon", "teaspoons"],
                        ["oz", "ounce", "ounces"],
                        ["fl oz", "fluid ounce"],
                        ["cup", "cups", "c"],
                        ["lb", "lbs", "pound", "pounds"]
                    ]

                    search_list = []

                    if recipe_unit in ["g", "gram", "grams"]:
                        final_grams = amount

                    for unit_list in unit_families:
                        if recipe_unit in unit_list:
                            search_list = unit_list
                            break

                    for row in portion_reader1:
                        if row[1] == id and row[6] in search_list:
                            portion_amount = float(row[3])
                            total_grams = float(row[7])

                            single_unit_weight = total_grams / portion_amount

                            final_grams = amount * single_unit_weight
                            break

                if final_grams > users_amount:
                    valid_recipe = False
                    break
        if valid_recipe:
            valid_recipes.append([recipe, data2])

    for recipe_pair in valid_recipes:
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(recipe_pair[0]["image"], use_container_width=True)
        with col2:
            st.subheader(recipe_pair[0]["title"])
            st.write("**Ingredients:**")

            missing_ingredients = []
            missing_ids = []

            for ingredient in recipe_pair[0]["missedIngredients"]:
                missing_ingredients.append(ingredient["original"])
                missing_ids.append(ingredient["id"])

            all_ingredients = []
            for ingredient in recipe_pair[1]["extendedIngredients"]:
                all_ingredients.append([ingredient["id"], ingredient["original"]])

            user_ingredients = []
            for ingredient in all_ingredients:
                if ingredient[0] not in missing_ids: 
                    user_ingredients.append(ingredient[1])

            for ingredient in user_ingredients:
                st.write(f"- {ingredient}")
            for ingredient in missing_ingredients:
                st.write(f"- {ingredient} *(missing)*")