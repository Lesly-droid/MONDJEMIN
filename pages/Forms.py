import streamlit as st
import Home
import audio as au

form = ""
all_data = ([[]], [])
st.title("Parlez-nous de ce que vous faites, Ça nous interesse :)")

with st.form("my_form"):
    # header = st.columns([1,2,2])
    # header[0].subheader('Color')
    # header[1].subheader('Opacity')
    # header[2].subheader('Size')

    # row1 = st.columns([1,2,2])
    # colorA = row1[0].color_picker('Team A', '#0000FF')
    # opacityA = row1[1].slider('A opacity', 20, 100, 50, label_visibility='hidden')
    # sizeA = row1[2].slider('A size', 50, 200, 100, step=10, label_visibility='hidden')

    # row2 = st.columns([1,2,2])
    # colorB = row2[0].color_picker('Team B', '#FF0000')
    # opacityB = row2[1].slider('B opacity', 20, 100, 50, label_visibility='hidden')
    # sizeB = row2[2].slider('B size', 50, 200, 100, step=10, label_visibility='hidden')
     # Question 1
    prenom = st.text_input("Quel est votre prénom ?", "")

    # Question 2
    nom = st.text_input("Quel est votre nom de famille ?", "")

    # Question 3
    adresse = st.text_input("Où habitez-vous ?", "")

    # Question 4
    contact = st.text_input("Quel est votre contact ?", "")

    # Question 5
    mail = st.text_input("Quel est votre e-mail ?", "")

    # Question 6
    savoir_faire = st.text_input("Quel savoir-faire possédez-vous (en 5 mots) ?", "")

    # Question 7
    talent_description = st.text_area("Décrivez brièvement votre talent", "")

    # Question 8
    talent_categorie = st.selectbox("Quel est sa catégorie ?", ["Art Culinaire", "Art Médical", "Art Plastiques", "Art Musical", "Autres"])

    mots_clés = st.text_area("Quels sont les mots-clés associés ? (séparés par des virgules)", "")

    # Question 9
    autres_infos = st.text_area("Avez-vous autres choses à nous dire ?", "")

    # Question 10
    nom_in = st.text_input("Nom et Prénom de l'Interviewer", "")
    
    fini = st.form_submit_button("J'ai fini")

    savoir_data = {
        "Nom : ": nom,
        "Prénom : ": prenom,
        "Adresse : ": adresse,
        "Contact : ": contact,
        "E-mail : ": mail,
        "Savoir-Faire : ": savoir_faire,
        "Description : ": talent_description,
        "Catégorie : ": talent_categorie,
        "Mots-Clés : " : mots_clés,
        "Nom et Prénom de l'Interviewer : ": nom_in,
        "Autres Informations : ": autres_infos
    }


if fini:
    with open(str(au.dossier_name + "/info.txt"), "w") as f:
            for question, reponse in savoir_data.items():
                f.write(f"{question}: {reponse}\n")
    # Call the function to copy the img folder
    au.copy_folder("/home/lesly/Hackaton/MONDJEMIN/img/", str(au.dossier_name + "/img/"))
    # Charger les images et leurs informations
    all_data = au.load_images()
    print("create_all_data")
    print(all_data)
    form = "finis"

if fini == "finis" and Home.traitement == "finis" :
    st.switch_page("gallery")


