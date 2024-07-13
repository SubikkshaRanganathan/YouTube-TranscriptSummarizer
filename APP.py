import streamlit as st
import spacy
import pytextrank
from PIL import Image,ImageOps,ImageDraw
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(layout="wide", page_title="YTS", page_icon="yt.png")

def summarize_transcript(video_id):
    has_transcript = check_transcript(video_id)
    if has_transcript:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        result = ""
        for i in transcript:
            result += ' ' + i['text']

        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe("textrank")
        s=""
        doc = nlp(result)
        for sent in doc._.textrank.summary(limit_phrases=2,limit_sentences=2):
             s += sent.text + " "

    else:
         s=""
         s = '''
                The Subtitles are disabled for this video.\n
                 So,it could not retreive transcript'''

    return s

def check_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return True
    except:
        return False
    
# Streamlit app code
def main():
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<h1 class='title'>YOUTUBE TRANSCRIPT SUMMARIZER</h1>", unsafe_allow_html=True)
    columns = st.columns([1,4])

    with columns[0]:
        logo_image = Image.open("logo.png") 
        square_logo = logo_image.resize((200, 200), resample=Image.LANCZOS)
        circular_mask = Image.new("L", square_logo.size, 0)
        draw = ImageDraw.Draw(circular_mask)
        draw.ellipse((0, 0, square_logo.size[0], square_logo.size[1]), fill=255)
        masked_logo = Image.new("RGBA", square_logo.size)
        masked_logo.paste(square_logo, (0, 0), mask=circular_mask)
        st.image(masked_logo, use_column_width=True)

    with columns[1]:
        col = st.columns([0.2,2,1])

        with col[1]:
            youtube_link =st.text_input("Enter YouTube Link:")
            if st.button("Summarize"):
                video_id = youtube_link.split("=")[-1]
                summarized_text = summarize_transcript(video_id)
                st.write(summarized_text)

if __name__ == "__main__":
    main()
