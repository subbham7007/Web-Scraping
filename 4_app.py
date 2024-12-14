## also  install the following Library
# use pip install -U streamlit pandas google-api-python-client


# To run the file use the Command : "streamlit run <your_file>"
import streamlit as st
import pandas as pd
import pickle
import numpy as np
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import re

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAhCHlGjsLfb0UmLpcvN7VUQQqWQmU9u2Y"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

hindi_pattern = re.compile(r'[\u0900-\u097F]')
bengali_pattern = re.compile(r'[\u0980-\u09FF]')
telugu_pattern = re.compile(r'[\u0C00-\u0C7F]')
tamil_pattern = re.compile(r'[\u0B80-\u0BFF]')
oriya_pattern = re.compile(r'[\u0B01-\u0B77]')
urdu_pattern = re.compile(r'[\u0600-\u06FF]')
# The rest of your code goes here...


# hindi_pattern = re.compile(r'[\u0900-\u097F]')
# bengali_pattern = re.compile(r'[\u0980-\u09FE]')
# telgu_pattern=re.compile(r'[\u0C00–\u0C7F]')
# tamil_pattern=re.compile(r'[\u0B80–\u0BFF]')
# oriya_pattern=re.compile(r'[\u0B01-\u0B77]')
# urdu_pattern=re.compile(r'[\u0600-\u06ff]')
def get_comments(video_id, max_comments,lang_name):
    comments = []
    st.write("Fetching Comments...")
    video_id=''.join(video_id)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=1000000000  # Max results per page
    )

    while request and len(comments) < max_comments:
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            if lang_name=="Hindi":
                if hindi_pattern.search(comment):
                    comments.append(comment)
            elif lang_name=="Oria":
                if oriya_pattern.search(comment):
                    comments.append(comment)
            elif lang_name=="Bengali":
                if bengali_pattern.search(comment):
                    comments.append(comment)
            elif lang_name=="Tamil":
                if tamil_pattern.search(comment):
                    comments.append(comment)
            elif lang_name=="Telugu":
                if telugu_pattern.search(comment):
                    comments.append(comment)
            elif lang_name=="Urdu":
                if urdu_pattern.search(comment):
                    comments.append(comment)
            if len(comments) >= max_comments:
                break
        request = youtube.commentThreads().list_next(request, response)

    return comments if len(comments)!=0 else ['No Comments in this language']



max_comments_per_video = 12000  # Number of comments to retrieve per video


st.title("YouTube Comment Classifier")
video_id=st.text_input("Enter the video id (from the link of the video take the part after (v=...))")
video_id=list(video_id)
selected_language_name = st.selectbox("What language you like to recommend?", ("English", "Hindi", "Oria","Bengali","Tamil","Telugu","Urdu"))
# st.button('Fetch Comments')
if st.button("Fetch Comments"):
    comments_fetched=get_comments(video_id,max_comments_per_video,selected_language_name)
    df=pd.DataFrame(comments_fetched, columns=['Comment'])
    st.write(df.shape[0]," Comment Fetched\n")
    st.write(df)
    # st.write()

# Install the following libraries
# Use pip install -U streamlit pandas google-api-python-client

# To run the file, use the command: "streamlit run <your_file>.py"
