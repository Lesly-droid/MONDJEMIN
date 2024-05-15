import os
import sys
import datetime
import shutil
from audio_recorder_streamlit import audio_recorder
import pickle
import time

dossier_name = ""
file_name = ""


def to_the_right_format(Data):
    # Unpack the two lists from Data
    list_of_lists, list_of_strings = Data

    # Initialize an empty dictionary
    result = {}

    # Iterate through both lists simultaneously using zip
    for A_list, B_str in zip(list_of_lists, list_of_strings):
        # Transform A_list to a tuple to be used as a dictionary key
        A_tuple = tuple(A_list)
        
        # Add the tuple and the corresponding string to the dictionary
        result[A_tuple] = B_str

    # Return the result  
    return(result)


def save_data_f(data, filepath):
    # Path to the file where the data will be saved
    file_path = filepath + 'data.pkl'
    data = to_the_right_format(data)
    # Open the file in write-binary mode and save the data
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)


def load_data_f():
    file_path = "/home/lesly/Hackaton/MONDJEMIN/data.pkl"
    # Open the file in read-binary mode and load the data
    with open(file_path, 'rb') as file:
        loaded_data = pickle.load(file)

    # Verify that the loaded data matches the original data
    return(to_the_right_format(loaded_data))

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

# Example condition check function
def check_conditions():
    time.sleep(5)  # Simulate checking conditions
    # Simulate a condition being met after 3 seconds
    return True

# Example long-running task function
def long_running_task():
    time.sleep(10)  # Simulate a 5-second task
    return "Task Completed"
