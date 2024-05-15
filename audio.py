import os
import sys
import datetime
import shutil
from audio_recorder_streamlit import audio_recorder

dossier_name = ""
file_name = ""
def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
        print(f"Dossier '{folder_name}' créé avec succès.")
    except FileExistsError:
        print(f"Le dossier '{folder_name}' existe déjà.")

def save_audio_file(audio_bytes, file_extension):
    """
    Save audio bytes to a file with the specified extension.

    :param audio_bytes: Audio data in bytes
    :param file_extension: The extension of the output audio file
    :return: The name of the saved audio file
    """
    global dossier_name, file_name

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audio_{timestamp}.{file_extension}"
    dossier_name = "Data" + str(timestamp)
    create_folder(dossier_name)
    file_name = str(dossier_name + "/" + filename)

    with open(str(file_name), "wb") as f:
        f.write(audio_bytes)

    return file_name

def load_images():

    base_path = '/home/lesly/Hackaton/MONDJEMIN/'

    # Listes pour stocker les chemins des images et le contenu des fichiers texte
    all_image_files = [[]]
    image_files = []
    text_contents = []

    # Parcourir tous les éléments dans le répertoire de base
    for entry in os.listdir(base_path):
        # Vérifier si l'entrée est un dossier et commence par "Data"
        if os.path.isdir(os.path.join(base_path, entry)) and entry.startswith('Data'):
            data_dir = os.path.join(base_path, entry)
            img_dir = os.path.join(data_dir, 'img')
            
            # Vérifier si le sous-dossier 'img' existe
            if os.path.exists(img_dir):
                # Parcourir tous les fichiers dans le sous-dossier 'img'
                for img_file in os.listdir(img_dir):
                    image_files.append(os.path.join(img_dir, img_file))
                all_image_files.append(image_files)
            # Parcourir tous les fichiers dans le dossier 'Data*' pour trouver des fichiers texte
            for file in os.listdir(data_dir):
                if file.endswith('.txt'):
                    file_path = os.path.join(data_dir, file)
                    with open(file_path, 'r') as f:
                        text_contents.append(f.read())
    
    return all_image_files, text_contents

# Fonction pour extraire la valeur associée à "Mots-Clés"
def extract_mots_cles(content):
    lines = content.split('\n')
    for line in lines:
        if line.startswith('Mots-Clés :'):
            return line.split('Mots-Clés :')[1].strip()
    return None


# Vérifier si un mot-clé est présent
def keyword_in_mots_cles(keyword,file_content):
    # Extraire les mots-clés
    mots_cles = extract_mots_cles(file_content)
    if mots_cles:
        return keyword.lower() in [mot.strip().lower() for mot in mots_cles.split(',')]
    return False


def copy_folder(src, dest):
    try:
        # Check if the source folder exists
        if not os.path.exists(src):
            print(f"The source folder '{src}' does not exist.")
            return
        
        # Check if the destination folder exists; if not, create it
        if not os.path.exists(dest):
            os.makedirs(dest)
        
        # Copy the folder and its contents
        shutil.copytree(src, dest, dirs_exist_ok=True)
        print(f"Folder '{src}' has been successfully copied to '{dest}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

