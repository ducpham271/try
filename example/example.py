import streamlit as st
from audiorecorder import audiorecorder
import datetime
import json
from google.oauth2 import service_account
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def save_ggdrive(audio):
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

# st.title("NỘI DUNG GHI ÂM GIỌNG NÓI ĐỐI VỚI NGƯỜI BỆNH PARKINSON")
st.header("NỘI DUNG GHI ÂM GIỌNG NÓI ĐỐI VỚI NGƯỜI BỆNH PARKINSON")

st.subheader("THÔNG TIN CÁ NHÂN:")
col1, col2 = st.columns([1, 3])  # Adjust column width ratios as needed
with col1:
    st.markdown("Họ tên:")
with col2:
    name = st.text_input("", key="name_input", label_visibility="collapsed") #collapse the label.

col3, col4 = st.columns([1, 3])
with col3:
    st.markdown("Năm sinh:")
with col4:
    year_of_birth = st.number_input("", min_value=1900, max_value=2025, step=1, key="yob", label_visibility="collapsed") #collapse the label.

col5, col6 = st.columns([1, 3])
with col5:
    st.markdown("Thời gian mắc bệnh Parkinson:")
with col6:
    years_parkinson = st.number_input("", min_value=0, step=1, key = "yop", label_visibility="collapsed") #collapse the label.

st.subheader("NỘI DUNG GHI ÂM:")
st.write("Nội dung 1: Phát âm nguyên âm “A” dài và lâu nhất có thể (2 lần)")
audio1 = audiorecorder("Ghi âm", "Ngừng ghi âm", "Tạm ngưng", custom_style={"backgroundColor": "lightblue"})
save_ggdrive(audio1)
