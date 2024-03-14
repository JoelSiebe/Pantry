import streamlit as st
import requests
import numpy as np
import pandas as pd

# CSS-Stil (https://discuss.streamlit.io/t/upload-background-image/59732 // https://www.w3schools.com/cssref/pr_background-image.php)
css_background = """   
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://i.postimg.cc/cJtrkLQw/pexels-mike-murray-5701888.jpg");
    background-size: cover;                 #grösse des hintergrundbilds, cover = ganzer container
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;        #beim scrollen fix oder bewegend - local = bewegend
}

[data-testid="stHeader"] {
    background: rgba(181, 179, 179);
}
</style>
"""

st.markdown(css_background, unsafe_allow_html=True) #css_background wird angewendet, unsafe für Anzeige von HTML-Inhalten

# Titel und Header
st.title("Pantry Pal - Conquering Leftovers, Mastering Meals",)
st.header("**Tame your kitchen with Pantry Pal**",)

# Versch. Zutaten des Benutzers als Eingabefeld
zutaten = st.text_input("Enter what's left in your fridge (separated by comma)")

#Filteroptionen (https://docs.streamlit.io/library/api-reference/widgets)

difficulty = st.selectbox("Select Difficulty", ["Any", "Easy", "Medium", "Hard"])
duration = st.selectbox("Select Cooking Time", ["Any", "0-15 minutes", "15-30 minutes", "30-60 minutes", "60+ minutes"])
number_ingredients = st.slider("Number of Ingredients", min_value=1, max_value=20, value=5)

if st.button('Show recipes'):
    if zutaten:

        # Spoonacular API-URL
        api_url = "https://api.spoonacular.com/recipes/findByIngredients"

        #API-Schlüssel (noch schauen, wie man das in einer anderen Datei macht)
        api_key = "06491aabe3d2435b8b21a749de46b765"

        #Datenbankabfrage (länder hinzufügen -> ?)
        parameter = {
            'ingredients': zutaten,
            'number': 5, #Anz. angezeigter Rezepte
            'apiKey': api_key
        }

        # Hinzufügen der Filteroptionen
        if difficulty != "Any":
            parameter['difficulty'] = difficulty.lower()
        if duration != "Any":
            if duration == "0-15 minutes":
                parameter['maxReadyTime'] = 15
            elif duration == "15-30 minutes":
                parameter['maxReadyTime'] = 30
            elif duration == "30-60 minutes":
                parameter['maxReadyTime'] = 60
            else:
                parameter['maxReadyTime'] = 60 

        if number_ingredients:
            parameter['number'] = number_ingredients

        #API-Abfrage senden
        response = requests.get(api_url, params=parameter)
        data = response.json()

        #Rezeptvorschläge 
        st.header("Look what we've found for you")
        for recipe in data:
            st.subheader(recipe['title'])
            st.image(recipe['image'])
            st.write(f"Used ingredients: {', '.join([ingredient['name'] for ingredient in recipe['usedIngredients']])}")
            st.write(f"Missing ingredients: {', '.join([ingredient['name'] for ingredient in recipe['missedIngredients']])}")
            st.write(f"Number of missing ingredients: {recipe['missedIngredientCount']}")
            st.write(f"Number of used ingredients: {recipe['usedIngredientCount']}")
  

            #Spoonacular-API für Rezeptinformationen (https://spoonacular.com/food-api/docs#Get-Recipe-Information) / Key ist derselbe
            api_informations_url = "https://api.spoonacular.com/recipes/{id}/information"
            
            if 'id' in recipe:  #API prüfen, ob Zubereitungschritte verfügubar 
                recipe_id = recipe['id']
                instructions_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
                instructions_response = requests.get(instructions_url, params={'apiKey': api_key})
                instructions_data = instructions_response.json()

                if 'instructions' in instructions_data:
                    st.subheader("Instructions:")
                    instructions = instructions_data['instructions'].split('\n')  
                    for step in instructions:
                        st.write(f"- {step}")  
                else:
                    st.write("Recipe steps not available.")

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")