import streamlit as st 
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

st.title('Sleep Analysis')

def parse_date(date_str):
    date_format = "%Y-%m-%d %I:%M%p"
    try:
        return pd.to_datetime(date_str, format=date_format)
    except ValueError:
        return date_str
    
# st.set_page_config(layout="wide", page_title="Sleep Insight - HealthInsight", page_icon="🩺")


sleep_csv = st.file_uploader("Choose a csv file", type="csv", help="Upload a csv file with sleep data from fitbit")

if sleep_csv is not None:
    with st.spinner("Loading the data..."):
        df = pd.read_csv(sleep_csv, skiprows=1)
        df['Start Time'] = df['Start Time'].apply(parse_date)
        df['End Time'] = df['End Time'].apply(parse_date)
        agent = create_pandas_dataframe_agent(GoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0.5, google_api_key=st.secrets["api_key"], safety_settings={ HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE}), df, verbose=True)
        st.write(str(agent.invoke("Provide Health Insight/Sleep report into the sleep data, and find patterns in the different columns excluding start and end time, provide details such as average sleep time, deep sleep etc. with accuracy")['output']))
        