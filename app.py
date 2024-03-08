import streamlit as st
import requests

# Hintergrundbild
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://i.postimg.cc/P5ksXpm2/pexels-vladimir-gladkov-6208084.jpg");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Stil (nochmals anschauen, teils redundat mit zuvor)
page_bg_img = """
<style>
body {
    background-image: url("https://i.postimg.cc/P5ksXpm2/pexels-vladimir-gladkov-6208084.jpg");
    background-size: cover;
}
.stApp {
    color: white;
    font-size: 40px; /* Ändere die Schriftgröße hier */
}
.text-input-container {
    font-size: 30px !important; /* Ändere die Schriftgröße des Eingabefeld-Textes */    
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Titel und Header
st.title("Pantry Pal - Conquering Leftovers, Mastering Meals",)
st.header("**Tame your kitchen with Pantry Pal**",)

# CSS Stil für Eingabefeld
st.write("""
<style>
div[data-baseweb="input"] input {
    color: black !important; /* Ändere die Schriftfarbe auf Schwarz */
    font-size: 20px !important; /* Ändere die Schriftgröße auf 20px */
}
</style>
""", unsafe_allow_html=True)

# Zutatenliste des Benutzers als Eingabefeld
zutaten = st.text_input("Enter what's left in your fridge (separated by comma)")

if zutaten:
    # Spoonacular API-URL
    api_url = "https://api.spoonacular.com/recipes/findByIngredients"

    #API-Schlüssel
    api_key = "06491aabe3d2435b8b21a749de46b765"

    #Datenbankabfrage
    parameter = {
        'ingredients': zutaten,
        'number': 5, #Anz. angezeiter Rezepte
        'apiKey': api_key
    }

    #API-Abfrage senden
    response = requests.get(api_url, params=parameter)
    data = response.json()

    #Rezeptvorschläge 
    st.header("Look what we've found for you")
    for recipe in data:
        st.subheader(recipe['title'])
        st.image(recipe['image'])
        st.write(f"Zutaten: {', '.join(recipe['usedIngredients'] + recipe['missedIngredients'])}")

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")
