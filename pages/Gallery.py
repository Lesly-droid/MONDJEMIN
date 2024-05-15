import streamlit as st
from PIL import Image
import os
import audio as au
import Home as h
import pages.Forms as f



# Fonction pour charger les images et leurs informations
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
    all_im, all_inf = f.all_data
    for img, inf in zip(all_im, all_inf):
        # if any(keywords.lower() in inf.lower().split()):
        if au.keyword_in_mots_cles(keywords, inf):
            filtered_images.append(img)
            filtered_info.append(inf)
    return filtered_images, filtered_info

# Filtrer les images si des mots-clés sont saisis
if search_keywords:
    filtered_images, filtered_info = filter_images_by_keywords(search_keywords)
else:
    filtered_images, filtered_info = f.all_data
    
# Affichage de la galerie d'images
selected_image_index = st.sidebar.radio("Sélectionnez une image", range(len(filtered_images)), format_func=lambda x: filtered_info[x])

if selected_image_index is not None:
    selected_image = filtered_images[selected_image_index]
    selected_info = filtered_info[selected_image_index]

    # Afficher l'image en grand
    st.image(selected_image[0], use_column_width=True)
    st.write(selected_info)

# Afficher les images de la galerie
st.sidebar.header("Galerie d'Images")
for img, inf in zip(filtered_images, filtered_info):
    st.sidebar.image(img[0], use_column_width=True, caption=inf)

