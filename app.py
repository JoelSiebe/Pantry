# Importieren der verschiedenen Bibliotheken
import streamlit as st
import requests
import matplotlib.pyplot as plt

# Titel und Header, Quelle für Header:https://stackoverflow.com/questions/70932538/how-to-center-the-title-and-an-image-in-streamlit
st.markdown("<h1 style='text-align: center; color: grey;'>Pantry Pal</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>Conquering Leftovers, Mastering Meals </h2>", unsafe_allow_html=True)
st.title("Tame your kitchen with Pantry Pal",)
st.divider()

# Bilder in 2 Kolonnen anzeigen, Quelle: https://docs.streamlit.io/library/api-reference/layout/st.columns)
st.header("So, what's the plan for today?")
st.header("Is it Italian? Or maybe a tasty burger?")
st.title("You decide.")
col1, col2= st.columns(2)

with col1:
   st.image("https://i.postimg.cc/44rnqrp3/pexels-lisa-fotios-1373915.jpgg") #Stock-Bild

with col2:
   st.image("https://i.postimg.cc/RZ0FH4BX/pexels-valeria-boltneva-1199957.jpg") #Stock-Bild

# Untertitel
st.header("How does it work?") 
st.header("First, enter what's left in your fridge. Selcect any filters if needed.")
st.title("Then let us do the magic")

#Filteroptionen (https://docs.streamlit.io/library/api-reference/widgets)

api_url = "https://api.spoonacular.com/recipes/findByIngredients" # Spoonacular API-URL
api_key = "06491aabe3d2435b8b21a749de46b765" # API-Schlüssel

# Funktion zum Abrufen von Rezepten mit den versch. Parametern
def get_recipes(ingredients, cuisine, difficulty, duration, allergies):
    parameter = {
        'ingredients': ingredients,
        'number': 1, # Anz. angezeigter Rezepte
        'apiKey': api_key
    }

# Filteroptionen
    if cuisine != "Any":
        parameter['cuisine']=cuisine
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

#API-Abfrage senden
    response = requests.get(api_url, params=parameter)
    return response.json()

# Daten-Visualisierung in Form eines Piecharts (auf Basis der Nährwerten:
# Funktion, um Infos aus API abzurufen und in data zu speichern
def get_nutrition_info(recipe_id):
    api_nutrition_url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    response = requests.get(api_nutrition_url, params={'apiKey': api_key})
    data = response.json()

# Funktion, um die Nährwerte als Float zurückzugeben (ansonsten funtioniert der Chart auf Streamlit nicht)
    def parse_nutrition_value(value):
        clean_value = ''.join([ch for ch in value if ch.isdigit() or ch == '.'])
        return float(clean_value)

 # Die relevanten Nährwerte (Kohlenhydrate, Protein, Fett) extrahieren und in Float umwandeln
    carbs = parse_nutrition_value(data['carbs'])
    protein = parse_nutrition_value(data['protein'])
    fat = parse_nutrition_value(data['fat'])

    return {'carbs': carbs, 'protein': protein, 'fat': fat}
   
# Zwei Texteingabefelder (Filteroptionen) nebeneinander anzeigen
with st.form(key='my_form'):
    col1, col2 = st.columns(2)
    with col1:
        ingredients = st.text_input('Ingredients')
        cuisine= st.selectbox('Cuisine', ['Any', 'African', 'Asian', 'American', 'Chinese', 'Eastern European', 'Greek', 'Indian', 'Italian', 'Japanese', 'Mexican', 'Thai', 'Vietnamese'])
    with col2:
        difficulty = st.selectbox('Difficulty Level', ['Any', 'Easy', 'Medium', 'Hard'])
        duration = st.selectbox('Duration', ['Any', '0-15 minutes', '15-30 minutes', '30-60 minutes', '60+ minutes'])
        allergies = st.selectbox('Allergies', ['None', 'Dairy', 'Egg', 'Gluten', 'Peanut', 'Seafood', 'Sesame', 'Shellfish', 'Soy', 'Tree Nut', 'Wheat'])

    submit_button = st.form_submit_button('Show recipes')

# Rezepte anzeigen, wenn die Schaltfläche "Show recipes" geklickt wird
if submit_button:
    if ingredients:
        recipes = get_recipes(ingredients, cuisine, difficulty, duration, allergies)
        if recipes:  # Wenn es Rezepte ausgibt
            for recipe in recipes:
                st.subheader(recipe['title'])  # Rezepttitel anzeigen
                st.image(recipe['image'])  # Bild des Rezepts anzeigen
                used_ingredients = ', '.join([ing['name'] for ing in recipe['usedIngredients']])
                missed_ingredients = ', '.join([ing['name'] for ing in recipe['missedIngredients']])
                st.write("Used Ingredients:", used_ingredients) # Gebrauchte und noch erforderliche Zutaten anzeigen
                st.write("Missing Ingredients:", missed_ingredients)
                
# Nährwertinformationen für das ausgewählte Rezept abrufen
                nutrition_data = get_nutrition_info(recipe['id'])

# Quelle für Workaround, um den Piechart kleiner zu machen: https://discuss.streamlit.io/t/cannot-change-matplotlib-figure-size/10295/10 
                col1, col2, col3, col4, col5=st.columns([1,1, 2, 1, 1])
                with col3:
                    labels = ['Carbohydrates', 'Protein', 'Fat']
                    sizes = [nutrition_data['carbs'], nutrition_data['protein'], nutrition_data['fat']]
                    colors = ['#133337', '#cccccc', '#6897bb']
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')  
                    st.pyplot(fig)

#  Spoonacular-API für Zubereitungsschritte der jeweiligen Rezepe (https://spoonacular.com/food-api/docs#Get-Recipe-Information)
                api_info_url = f"https://api.spoonacular.com/recipes/{recipe['id']}/information"
                instructions_response = requests.get(api_info_url, params={'apiKey': api_key})
                instructions_data = instructions_response.json()

                if 'analyzedInstructions' in instructions_data:
                    steps = instructions_data['analyzedInstructions']
                    if steps: 
                        st.subheader("Instructions:")
                        for section in steps:
                            for step in section['steps']:
                                st.write(f"Step {step['number']}: {step['step']}")  # Detaillierte Schritte anzeigen
                    else:
                        st.write("No detailed instructions found.")
                else:
                    st.write("No instructions available.")  
            else:
                st.write("No recipes found for the given ingredients.") 

# Fusszeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal - Where Leftovers Meets Deliciousness. All rights reserved.")