from transformers import pipeline
from pydub import AudioSegment
import os
from typing import Union
import torch
import requests
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from huggingface_hub import login
from huggingface_hub import hf_hub_download
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


login(token = "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")

tokenizer_tr = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1", padding_side="left")

model_tr = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1", device_map="auto")


pipe = pipeline("automatic-speech-recognition", model="Zelyanoth/wav2vec2-bert-fon-colab")

from huggingface_hub import hf_hub_download
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "facebook/nllb-200-distilled-600M", token=True, src_lang="fon_Latn"
)
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
# model_alt = model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-3.3B")

def translate(inputt) :
    lop = []
    for a in input :
        tokenizer = AutoTokenizer.from_pretrained(
                "facebook/nllb-200-distilled-600M", token=True, src_lang="fon_Latn"
            )
        model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M", token=True)
        inputs = tokenizer(inputt, return_tensors="pt")

        translated_tokens = model.generate(
                **inputs, forced_bos_token_id=tokenizer.lang_code_to_id["fra_Latn"], max_length=500
        )
        lop.append(tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0])
    return ' '.join(lop)

def formater(nom_fichier_m4a, nom_fichier_wav):
        "permet de formatter le fichier pour qu il soit gérable par le transcripteur c est son bro sure"
        formats = os.path.splitext(nom_fichier_m4a)[1][1:]
        audio = AudioSegment.from_file(nom_fichier_m4a, format=formats)
        audio.export(nom_fichier_wav, format="wav")
        audio = AudioSegment.from_wav(nom_fichier_wav)
        duree_audio_ms = len(audio)
        duree_segment_ms = 40000
        if duree_audio_ms > duree_segment_ms :
            segments_audio = []
            debut_segment = 0
            fin_segment = duree_segment_ms
            while debut_segment < duree_audio_ms:
                segment = audio[debut_segment:fin_segment]
                nombre_dossiers = 0
                chemin_dossier = "./working/"
                for element in os.listdir(chemin_dossier):
                    # Vérifier si l'élément est un dossier
                    if os.path.isdir(os.path.join(chemin_dossier, element)):
                        # Incrémenter le compteur
                        nombre_dossiers += 1
                folder = "./working/split"+str(nombre_dossiers)
                os.mkdir(folder)
                outputfile = "./working/split"+str(nombre_dossiers)+"/"+nom_fichier_wav+ str(fin_segment)
                segment.export(outputfile , format="wav")
                segments_audio.append(outputfile )

                # Mettre à jour les indices pour le prochain segment
                debut_segment = fin_segment
                fin_segment += duree_segment_ms
                
            return segments_audio
        else : 
            return "/kaggle/working/"+nom_fichier_wav



def transcriptor(audio : Union[str, list]) :
    "Fais une transcription de l audio en fon nyehehe"
    global pipe 
    if isinstance(audio, list) :
        trans = []
        for a in audio : 
            transcription = pipe(a)
            trans.append(transcription['text'])
        transcr = " ".join(trans)
        return transcr
    else :
        transcription = pipe(audio)
        return transcription(['text'])

def generate_image(process) : 
    stored = []
    for pomrp in process :

        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/core",
            headers={
                "authorization": f"Bearer sk-duJKGQfp30cYqYuI8JdXo1c70mliv4YDgMizHlo3jvFGVQDP",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": "{}".format(pomrp),
                "output_format": "webp",
            },
        )

        if response.status_code == 200:
            path = "./image_audio_1"+a+".webpp"
            with open(path, 'wb') as file:
                file.write(response.content)
            stored.append([path,pomrp])
        else:
            raise Exception(str(response.json()))
    return stored



def extract_information(texte):
    for a in ["""S il te plait ce texte est probablement {}
  jonchés d erreur de sémantique, d orthographe etc s il te plaît corrige tout ça 
                """.format(texte),"""
                        Il y un processus dans ce texte  {}, trouves et extrait les differentes etapes de ce processus en allant à la ligne pour chaque etape
                    n'ecrit que ça dans ta réponse et au debut de chaque étape on doit pouvoir avoir des * """.format(responses)] :
        model_inputs_tr = tokenizer([a], return_tensors="pt").to("cuda")
        generated_ids = model.generate(model_inputs_tr)
        responses = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    segments = []

    # Variable pour stocker temporairement les mots d'un segment
    current_segment = []

    # Diviser la chaîne en mots
    words = responses.split()

    # Parcourir chaque mot de la liste
    for word in words:
        if word.startswith('*'):
            # Si on rencontre un mot commençant par '*', ajouter le segment actuel à la liste des segments
            if current_segment:
                segments.append(' '.join(current_segment))
            # Commencer un nouveau segment
            current_segment = [word]
        else:
            # Sinon, ajouter le mot actuel au segment en cours
            current_segment.append(word)

# Ajouter le dernier segment s'il existe
    if current_segment:
        segments.append(' '.join(current_segment))

    return segments


for word in words:
    if word.startswith('*'):
        # Si on rencontre un mot commençant par '*', ajouter le segment actuel à la liste des segments
        if current_segment:
            segments.append(' '.join(current_segment))
        # Commencer un nouveau segment
        current_segment = [word]
    else:
        # Sinon, ajouter le mot actuel au segment en cours
        current_segment.append(word)

# Ajouter le dernier segment s'il existe
if current_segment:
    segments.append(' '.join(current_segment))

print(segments)


def run_boy_run() :   
    "return in order the transcription, the traduction, and the extracted information, MOUAHAHA staaaaaand power"
    tt = input()
    mm = formater(tt, "test.wav")
    print(mm)
    source_sentence = transcriptor(mm)
    print(source_sentence)
    segment = []
    for i in range(0, len(source_sentence), 30):
        segment.append(source_sentence[i:i + 30])

    traduction = translate(source_sentence)
    print(traduction)
    process = extract_information(traduction)
    print(process)
    step  = extract_information(traduction)
    image_generation = generate_image(step)
    return  source_sentence, traduction ,process,image_generation
    

run_boy_run()



