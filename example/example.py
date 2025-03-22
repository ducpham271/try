import streamlit as st
from audiorecorder import audiorecorder
import datetime
import json
from google.oauth2 import service_account
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# def replace_micro_sign(input_string):
#     return input_string.replace('\xb5', 'µ')  # \xb5 is the Latin-1 micro sign
# def remove_micro_sign(input_string):
#     return input_string.replace('\xb5', '')
st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Click to stop recording", custom_style={"backgroundColor": "lightblue"})

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio.export().read())

    # To save audio to a file, use pydub export method:
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    filename = f"audio_{timestamp}.wav"

    audio.export(filename, format="wav")
    print(filename)
    st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")
    my_string = st.secrets["SERVICE_ACCOUNT_JSON"]
    # cleaned_string = replace_micro_sign(my_string)
    service_account_info = json.loads(my_string)
    
    
    creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=['https://www.googleapis.com/auth/drive.file'])
    # Google Drive Upload
    drive_folder_id = st.secrets["DRIVE_FOLDER_ID"]  # Get from Streamlit secrets

    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': filename,
        'parents': [drive_folder_id]
    }

    media = MediaFileUpload(filename, mimetype='audio/wav')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    st.success(f"File '{filename}' uploaded to Google Drive folder with ID: {drive_folder_id}")
    print(f"File ID: {file.get('id')}")

    # Clean up the local file after upload
    os.remove(filename)
