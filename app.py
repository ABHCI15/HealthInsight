import streamlit as st 
import pathlib
import textwrap
import google.generativeai as genai

st.set_page_config(layout="wide", page_title="HealthInsight", page_icon="🩺")
# AIzaSyAC2aMax9s7ev0ZGRFvNn6YlsrkM2c5ahc
genai.configure(api_key=st.secrets["api_key"])
model = genai.GenerativeModel('gemini-pro')

st.title("HealthInsight V 0.01.0")

