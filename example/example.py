import streamlit as st
from audiorecorder import audiorecorder
import datetime
import json
from google.oauth2 import service_account
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

st.title("Ghi âm giọng nói")

# # Input Name
# name = st.text_input("Name:")

# # Input Year of Birth
current_year = datetime.datetime.now().year
# year_of_birth = st.number_input("Year of Birth:", min_value=1900, max_value=current_year, step=1)

# # Input Number of Years with Parkinson's
# years_with_parkinson = st.number_input("Number of Years with Parkinson's:", min_value=0, step=1)

# # Display the information (optional)
# if name and year_of_birth is not None and years_with_parkinson is not None: #check if all fields are filled.
#     age = current_year - year_of_birth
#     st.write(f"Name: {name}")
#     st.write(f"Age: {age}")
#     st.write(f"Years with Parkinson's: {years_with_parkinson}")
# elif name or year_of_birth is not None or years_with_parkinson is not None:
#     st.warning("Please fill out all fields.")

# # Example with collapsed labels:

# st.subheader("Collapsed Labels Example")

name_collapsed = st.text_input("Họ tên:", label_visibility = "collapsed", placeholder = "Họ tên")
year_collapsed = st.number_input("Năm sinh", min_value=1930, max_value=2007, step=1, label_visibility = "collapsed", placeholder = "Năm sinh")
years_collapsed = st.number_input("Thời gian mắc bệnh Parkinson:", min_value=0, step=1, label_visibility = "collapsed", placeholder = "Thời gian mắc bệnh Parkinson")


if name_collapsed and year_collapsed is not None and years_collapsed is not None:
    age_collapsed = current_year - year_collapsed
    st.write(f"Họ tên: {name_collapsed}")
    st.write(f"Tuổi: {age_collapsed}")
    st.write(f"Thời gian mắc bệnh Parkinson: {years_collapsed}")
elif name_collapsed or year_collapsed is not None or years_collapsed is not None:
    # st.warning("Please fill out all fields.")
    pass


audio = audiorecorder("Ghi âm", "Ngừng ghi âm", "Tạm ngưng", custom_style={"backgroundColor": "lightblue"})

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
    service_account_info = json.loads(st.secrets["SERVICE_ACCOUNT_JSON"])
    
    
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

    st.success(f"Ghi âm '{filename}' đã được lưu vào Google Drive")
    print(f"File ID: {file.get('id')}")

    # Clean up the local file after upload
    os.remove(filename)
