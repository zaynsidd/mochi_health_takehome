import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.title("Mood Board")

if "sheet" not in st.session_state:
    #Google Sheets connection setup (making sure not to make too many API calls)
    creds_dict = dict(st.secrets["gcp_service_account"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    st.session_state.scopes = scopes
    st.session_state.creds = credentials
    st.session_state.client = gspread.authorize(credentials)
    st.session_state.sheet_id = "15HeXDtE9wtn_rkmTvWSFpR7SrAVRWCZFxfLT0J-sd-c"
    st.session_state.sheet = st.session_state.client.open_by_key(st.session_state.sheet_id).sheet1
    
    #Date initialization and sanitization to string
    st.session_state.date = str(datetime.now())[:10]


#Initialization of values that need to be reinstantiated, or do not have much overhead to rerun each time
form_values = {
    'mood': None,
    'note': None, 
    'time': None
}
moods = ['Excited', 'Anxious', 'Joyful', 'Frustrated', 'Indifferent', 'Sad']

#Main form logic
with st.form(key = "mood_form"):
    form_values['mood'] = st.selectbox("Choose your mood:", moods)
    form_values['note'] = st.text_area("Leave a note describing your mood:")

    submission = st.form_submit_button(label = 'Submit')

    if submission:
        form_values['date'] = str(datetime.now())[:10]
        if not form_values['mood'] or not form_values['note']:
            st.warning("Please fill in all fields!")
        else:
            st.session_state.sheet.append_row([form_values['date'], form_values['mood'], form_values['note']])
            st.write("Thanks for sharing!")

#Bar chart logic and data organization
df = pd.DataFrame(st.session_state.sheet.get_all_records())
st.write(df.tail(10))
df_filtered = df[df['Date']==st.session_state.date]

st.subheader("Mood Frequencies for " + st.session_state.date)
fig, ax = plt.subplots()
plt.xlabel('Mood')
plt.ylabel('Frequencies on '+ st.session_state.date)
mood_counts = df_filtered['Mood'].value_counts()
mood_counts = [mood_counts.get(mood, 0) for mood in moods]
plt.bar(moods, mood_counts)
st.pyplot(fig)

with st.form(key='date_change'):
    selected_date = st.date_input('Select another date to view')
    submit = st.form_submit_button(label='Change Date')

    if submit:
        st.session_state.date = str(selected_date)
