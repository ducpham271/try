import streamlit as st
from audiorecorder import audiorecorder
import datetime
import json
from google.oauth2 import service_account
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def save_ggdrive(audio, _name, _year_of_birth, _years_parkinson):
    # To play audio in frontend:
    st.audio(audio.export().read())

    # To save audio to a file, use pydub export method:
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    filename = f"{_name}_{_year_of_birth}_{_years_parkinson}_{timestamp}.wav"

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

st.markdown(
    """
    <style>
    h1 {
        font-size: 24px;  /* Adjust the size here */
    }
    [data-testid="stColumn"] {
        padding: 0px !important;
    }
    label {
        font-size: 14px; /* Reduced label font size */
        margin-bottom: 2px; /* Reduced margin */
    }
    input, [data-baseweb="input"], [data-baseweb="input-container"] {
        font-size: 14px; /* Reduced input font size */
        padding: 4px; /* Reduced padding */
        margin-bottom: 4px; /* Reduced margin */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.subheader("NỘI DUNG GHI ÂM GIỌNG NÓI ĐỐI VỚI NGƯỜI BỆNH PARKINSON")

st.markdown("THÔNG TIN CÁ NHÂN:")

col1, col2 = st.columns([1, 2])
with col1:
    st.write("Họ tên:")
with col2:
    name = st.text_input("", key="name_input", label_visibility="collapsed")

col3, col4 = st.columns([1, 2])
with col3:
    st.write("Năm sinh:")
with col4:
    year_of_birth = st.number_input("", min_value=1900, max_value=2025, step=1, key="yob", label_visibility="collapsed")

col5, col6 = st.columns([1, 2])
with col5:
    st.write("Số năm mắc bệnh Parkinson:")
with col6:
    years_parkinson = st.number_input("", min_value=0, step=1, key="yod", label_visibility="collapsed")

st.markdown("NỘI DUNG GHI ÂM:")
st.write("1. Phát âm nguyên âm “A” dài và lâu nhất có thể (lần 1)")
audio1 = audiorecorder("Ghi âm", "Ngừng ghi âm", custom_style={"backgroundColor": "lightblue"}, key="ghiam1")
if len(audio1) > 0:
    save_ggdrive(audio1, name, year_of_birth, years_parkinson)
st.write("2. Phát âm nguyên âm “A” dài và lâu nhất có thể (lần 2)")
audio2 = audiorecorder("Ghi âm", "Ngừng ghi âm", custom_style={"backgroundColor": "lightblue"}, key="ghiam2")
if len(audio2) > 0:
    save_ggdrive(audio2, name, year_of_birth, years_parkinson)
st.write("3. Phát âm nguyên âm “A” dài và lâu nhất có thể (lần 3)")
audio3 = audiorecorder("Ghi âm", "Ngừng ghi âm", custom_style={"backgroundColor": "lightblue"}, key="ghiam3")
if len(audio3) > 0:
    save_ggdrive(audio3, name, year_of_birth, years_parkinson)