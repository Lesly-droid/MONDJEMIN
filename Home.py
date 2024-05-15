import streamlit as st
from audio_recorder_streamlit import audio_recorder
from streamlit_extras.switch_page_button import switch_page
import audio as au
import time

traitement = ""

st.set_page_config(
    page_title="Multipage App",
    page_icon="👋",
)

st.title("Main Page")
# st.sidebar.success("Select a page above.")

tab1, tab2 = st.tabs(["Je préfère enregistrez sur l'application", "Non merci, mais j'ai mon audio"])

# Record Audio tab
with tab1:
    audio_bytes = audio_recorder(pause_threshold=30, sample_rate=16_000,
    text="",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_size="6x")


# Upload Audio tab
with tab2:
    audio_file = st.file_uploader("Charger l'audio", type=["mp3", "mp4", "wav", "m4a"])



submit = st.button("Soumettre")
if submit:
    if audio_file:
        au.save_audio_file(audio_file.read(), "wav")
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        au.save_audio_file(audio_bytes, "wav")
    switch_page("forms")
    traitement = "en cours"

time.sleep(0.5)

traitement = "finis"
