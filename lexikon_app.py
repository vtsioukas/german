import streamlit as st
import random
import pandas as pd

# Ρύθμιση σελίδας
st.set_page_config(page_title="Εκμάθηση Γερμανικών", layout="centered")

# Συνάρτηση για ανάγνωση του αρχείου
def load_data():
    words = []
    try:
        with open("lexiko.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "," in line:
                    ger, gr = line.strip().split(",")
                    words.append({"German": ger, "Greek": gr})
    except FileNotFoundError:
        st.error("Το αρχείο lexiko.txt δεν βρέθηκε!")
    return words

data = load_data()

st.title("🇩🇪 Τα Γερμανικά μου")
tab1, tab2, tab3 = st.tabs(["Ελληνικά -> Γερμανικά", "Γερμανικά -> Ελληνικά", "Τέστ Γνώσεων"])

import requests

# ΚΑΡΤΕΛΑ 1: Ελληνικά -> Γερμανικά (Με Εικόνα)
with tab1:
    st.subheader("Μελέτη με Εικόνες")
    for item in data:
        with st.expander(f"Πώς λέμε: {item['Greek']};"):
            word = item['German']
            
            # Αναζήτηση εικόνας μέσω Wikipedia API (γερμανική)
            url = f"https://de.wikipedia.org/w/api.php?action=query&titles={word}&prop=pageimages&format=json&pithumbsize=400"
            try:
                response = requests.get(url, timeout=3).json()
                pages = response.get("query", {}).get("pages", {})
                page = list(pages.values())[0]
                
                if "thumbnail" in page:
                    image_url = page["thumbnail"]["source"]
                    st.image(image_url, caption=f"Εικόνα για: {word}")
                else:
                    st.info(f"Δεν βρέθηκε ακριβής εικόνα για: {word}")
            except Exception:
                st.info(f"Δεν βρέθηκε εικόνα για: {word}")
                
            st.write(f"### **{word}**")

# ΚΑΡΤΕΛΑ 2: Γερμανικά -> Ελληνικά
with tab2:
    st.subheader("Μετάφραση στα Ελληνικά")
    df = pd.DataFrame(data)
    st.table(df)

# ΚΑΡΤΕΛΑ 3: Κουίζ Πολλαπλής Επιλογής
with tab3:
    st.subheader("Ώρα για Τέστ!")
    
    if len(data) < 4:
        st.warning("Απαιτούνται τουλάχιστον 4 λέξεις στο lexiko.txt για να ξεκινήσει το κουίζ.")
    else:
        if "current_question" not in st.session_state:
            st.session_state.current_question = random.choice(data)
            # Δημιουργία επιλογών (η σωστή + 3 τυχαίες)
            others = [d['German'] for d in data if d['German'] != st.session_state.current_question['German']]
            options = random.sample(others, 3) + [st.session_state.current_question['German']]
            random.shuffle(options)
            st.session_state.options = options

        q = st.session_state.current_question
        st.write(f"### Ποια είναι η μετάφραση για τη λέξη: **{q['Greek']}**")
        
        answer = st.radio("Επιλέξτε το σωστό:", st.session_state.options)
        
        if st.button("Έλεγχος"):
            if answer == q['German']:
                st.success("Μπράβο! Σωστά!")
            else:
                st.error(f"Λάθος. Το σωστό είναι: {q['German']}")
            
        if st.button("Επόμενη Λέξη"):
            del st.session_state.current_question
            st.rerun()