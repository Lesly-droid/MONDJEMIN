import keyword
import streamlit as st
from PIL import Image
import os
import audio as au
import Home as h
import pages.Forms as f 
import time

all_data = au.load_data_f()
# all_data = {k: v for k, v in all_data.items() if k and v}
print(all_data)

#Fonction pour charger les images et leurs informations
# def load_images_and_info():
#     images = []
#     info = []
    
#     # Exemple de structure de données
#     # Remplacez cette partie par votre propre logique de chargement des images et informations
#     images_dir = str(au.dossier_name +  "/img/")
#     for filename in os.listdir(images_dir):
#         if filename.endswith(".jpg") or filename.endswith(".png"):
#             img_path = os.path.join(images_dir, filename)
#             images.append(img_path)
#             # Informations associées à chaque image
#             with open(str(au.dossier_name + "/info.txt"), 'r') as file:
#                 content = file.read()
#             info.append(content)
#     return images, info



# Interface utilisateur Streamlit
st.title("Galerie d'Images")

# Recherche par mots-clés
search_keywords = st.text_input("Rechercher par mots-clés")

# Fonction pour filtrer les images par mots-clés
def filter_images_by_keywords(keywords):
    filtered_images = [[]]
    filtered_info = []
    # all_im, all_inf = all_data
    for img, inf in all_data.items():
        # if any(keywords.lower() in inf.lower().split()):
        if au.keyword_in_mots_cles(keywords, inf):
            filtered_images.append(img)
            filtered_info.append(inf)
    d = filtered_images, filtered_info
    return au.to_the_right_format(d)

# Filtrer les images si des mots-clés sont saisis
if search_keywords:
    d = filter_images_by_keywords(search_keywords)
else:
    d = all_data

# Get the keys of the dictionary
keys = list(all_data.keys())

# Sidebar radio button to select an image key
selected_key = st.sidebar.radio("Sélectionnez une image", keys)


if selected_key is not None:
    selected_image = selected_key
    selected_info = all_data[selected_key]

    # Afficher l'image en grand
    if(selected_image):
        for i in range(len(selected_image)):
            time.sleep(5)
            st.image(selected_image[i], use_column_width=True, caption=selected_info)
    #st.write(selected_info)

# Afficher les images de la galerie
st.sidebar.header("Galerie d'Images")
for img, inf in all_data.items():
    st.sidebar.image(img[0], use_column_width=True, caption=inf)

