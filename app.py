import json
import os

import streamlit as st
from dotenv import load_dotenv

from scripts.utils import clean_video_url, examples, show_output, transcribe_video

st.set_page_config(layout="wide")
load_dotenv()

analysis_choice = st.sidebar.radio(
    "Start trascribing",
    ["Discover some examples", "Upload your own YouTube video"],
)


if analysis_choice == "Discover some examples":
    use_topic_detection = True
    titles = list(examples.keys())
    selected_title = st.sidebar.selectbox("Select a video", options=titles)

    video_url = examples[selected_title]["video_url"]
    video_name = examples[selected_title]["name"]
    video_name = video_name.replace(" ", "_")

    with open(f"./transcripts/{video_name}.json", "r") as f:
        transcript = json.load(f)

    show_output(video_url, transcript, use_topic_detection)


elif analysis_choice == "Upload your own YouTube video":

    try:
        API_KEY = "84b10466cfdf4f52ab4c349a161cedaa"
    except:
        API_KEY = None

    if API_KEY is None:
        API_KEY = os.environ.get("x", None)

    if API_KEY is None:
        st.error("You must provide an AssemblyAI key.")
        st.markdown(
            """
            It's simple, you can either:
            - add a `.env` file with an API_KEY key (you can do this to try out the app locally)
            - add your API_KEY as Streamlit secret and load it via the `st.streamlit` method
        """
        )
        st.stop()

    video_url = st.sidebar.text_input("Enter youtube video")
    video_url = clean_video_url(video_url)

    if video_url.strip() != "":
        use_content_moderation = st.sidebar.checkbox("Use content moderation", value=False)
        use_topic_detection = st.sidebar.checkbox("Use topic detection", value=True)

        transcribe_button = st.sidebar.button("Transcribe audio")

        if transcribe_button:
            transcript = transcribe_video(
                video_url,
                use_content_moderation,
                use_topic_detection,
            )
            show_output(video_url, transcript, use_topic_detection)
