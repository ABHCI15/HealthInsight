import streamlit as st 
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
import plotly.express as px
from tools import *

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)



def parse_date(date_str):
    date_format = "%Y-%m-%d %I:%M%p"
    try:
        return pd.to_datetime(date_str, format=date_format)
    except ValueError:
        return date_str
    
# st.set_page_config(layout="wide", page_title="Sleep Insight - HealthInsight", page_icon="🩺")
@st.cache_data
def AIGen(sleep_csv):
    with st.spinner("Loading the data..."):
        df = pd.read_csv(sleep_csv, skiprows=1)
        df['Start Time'] = df['Start Time'].apply(parse_date)
        df['End Time'] = df['End Time'].apply(parse_date)
        agent = create_pandas_dataframe_agent(GoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0.5, google_api_key=st.secrets["api_key"], safety_settings={ HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE}), df, verbose=True)
        return str(agent.invoke("Provide Health Insight/Sleep report into the sleep data, and find patterns in the different columns excluding start and end time, provide details such as average sleep time, deep sleep etc. with accuracy")['output'])



@st.cache_data
def simpleGraph(df):
    st.scatter_chart(df, x="Number of Awakenings", y="Time in Bed")

@st.cache_data
def AIgenScatter(sleep_csv):
    df = pd.read_csv(sleep_csv, skiprows=1)
    df['Start Time'] = df['Start Time'].apply(parse_date)
    df['End Time'] = df['End Time'].apply(parse_date)
    agent = create_pandas_dataframe_agent(GoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0.5, google_api_key=st.secrets["api_key"], safety_settings={ HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE}), df, verbose=True, extra_tools=[graphAgent])
    return str(agent.invoke("use the tools provided and generate a simple scatter chart, then provide a simple description of what the chart depicts.")['output'])

if 'user_info' in st.session_state:
    st.title('Sleep Analysis')
    sleep_csv = st.file_uploader("Choose a csv file", type="csv", help="Upload a csv file with sleep data from fitbit")

    # makes sure a csv file is uploaded
    if sleep_csv is not None:
        buttonAiGen = st.button("Generate Gemini Insight") 
        buttonGraph = st.button("Generate Graphs")
        buttonAiGenScatter = st.button("Generate Gemini Scatter Chart")
        # a simple scatter chart
        if buttonAiGenScatter:
            st.write(AIgenScatter(sleep_csv))
        if buttonGraph:
            df = pd.read_csv(sleep_csv, skiprows=1)
            simpleGraph(df)
 # a simple template scatter chart
        if buttonAiGen:
            st.write(AIGen(sleep_csv)) # uses gemini to query the pandas object and analyzes the file

else:
    st.write("Please login to access this page")
    st.switch_page("app.py")


