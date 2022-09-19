#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)

client = gspread.authorize(credentials)
# Open the spreadhseet
sheet = client.open("DFIA").worksheet("Samples")
sheet_fd = client.open("DFIA").worksheet("Feedback")

# In[6]:


df = pd.DataFrame(sheet.get_all_records())


# In[ ]:


st.set_page_config(layout="wide")
st.title("Model Feedback Dashboard")
st.subheader("Based on Plot and Scores Dashboard, Please Record Your Feedback Here!")
signal_id = st.selectbox('Select a Signal ID', list(df["user_id"]),key="signal_id_m")
st.caption("You Selected " + str(signal_id)+"!")
st.write("Description for Selected Signal: " + df[df["user_id"] == signal_id]["Desc"].values[0])
st.write("Please Provide Your Feedback on the Following Scores!")
input_options = ["High","Optimal","Low"]

col1, col2 = st.columns(2)

with col1:
    po = st.radio("Power Score",input_options, horizontal = True, key = "po")
    sm = st.radio("Sudden Jerks",input_options, horizontal = True, key = "sm")
    jm = st.radio("Jittering",input_options, horizontal = True, key = "jm")
    it = st.radio("Inconsistent Tempo",input_options, horizontal = True, key = "it")

with col2:
    bjm = st.radio("Blip Jittering",input_options, horizontal = True, key = "bjm")
    sta = st.radio("Stamina Score",input_options, horizontal = True, key = "sta")
    rep = st.radio("Rep Score",input_options, horizontal = True, key = "rep")
    ufs = st.radio("User Form Score",input_options, horizontal = True, key = "ufs")

ac = st.text_input("Additional Comments", key = "ac")

if st.button("Save Feedback",key="Save_Feedback"):
    sheet_fd.append_row([signal_id,po,sm,jm,it,bjm,sta,rep,ufs,ac],value_input_option="USER_ENTERED")
    st.write("Sample Appended for ID: " + str(signal_id) + " to Database! Please Add the next Sample!")    

