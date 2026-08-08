import streamlit as st
import csv
import requests

st.write("Welcome to the recipe recommender!")

st.write("Write an ingredient you would like to use. Please be specific.")
ingredients = st.text_input("Tip: Its recommended to use keywords like 'raw', 'cooked', 'fresh', 'frozen' or specific cuts like 'ground' or 'breast'.")

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
                    scored_results.append((score, row[2]))
            scored_results.sort(reverse=True)

            st.write("Top Results:")

            if 'selected' not in st.session_state:
                st.session_state.selected = {}

            for i in range(min(5, len(scored_results))):
                ingredient_name = scored_results[i][1]
                
                if st.button(f"Add {ingredient_name}"):
                    if ingredient_name not in st.session_state.selected:
                        st.session_state.selected[ingredient_name] = 0
                        st.rerun()

            st.write("Selected Ingredients:")
            for item in list(st.session_state.selected.keys()):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"{item}")
                    
                with col2:
                    units = {}
                    with open('food_portion.csv', mode='r', encoding='utf-8') as file1, \
                        open('food.csv', mode='r', encoding='utf-8') as file2:
                        portion_reader = csv.reader(file1)
                        id_reader = csv.reader(file2)
                        next(portion_reader)
                        next(id_reader)
                        
                        for row in id_reader:
                            description = row[2].lower()
                            if description == item.lower():
                                id = row[0]

                        for row in portion_reader:
                            if row[1] == id:
                                portion_amount = float(row[3])
                                unit_name = row[6]
                                total_grams = float(row[7])

                                if unit_name and portion_amount > 0:
                                    single_unit_weight = total_grams / portion_amount
                                    units[unit_name] = single_unit_weight

                    selected_unit = st.selectbox("Unit:", list(units.keys()), index=None, placeholder="Select unit...")

                with col3:
                    current_amount = st.session_state.selected[item]
                    new_amount = st.number_input("Value:", min_value=0.0, value=float(current_amount), step=1.0, key=f"amount_{item}")
                    if selected_unit:
                        gram_amount = new_amount * units.get(selected_unit)
                        st.session_state.selected[item] = gram_amount
                        st.write(f"Amount in grams: {gram_amount:.2f}")
                      
                with col4:
                    if st.button("Remove", key=f"remove_{item}"):
                        del st.session_state.selected[item]
                        st.rerun()

API_KEY = "" # Need to hide this

if st.button("Find Recipes"):
    pass # API logic goes here