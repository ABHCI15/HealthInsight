import streamlit as st 
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# import pandas as pd
# import plotly.express as px
from langchain_core.tools import Tool
# from langchain_experimental.utilities import PythonREPL
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools.tavily_search import TavilySearchResults
import os 
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain_core.prompts import PromptTemplate

os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
# TavilySearchAPIWrapper = TavilySearchAPIWrapper(tavily_api_key=st.secrets["TAVILY_API_KEY"])
tool_med = PubmedQueryRun()
tool_search = TavilySearchResults()


st.title("Medical Help Chatbot")

with st.chat_message("assistant"):
    st.write("Hello 👋, Welcome to Med Q&A, please note that this is not intended to provide medical advice and merely exists as a small research aid.")

text = st.chat_input(placeholder="Type your message here...")
template = """
    Answer the following questions as best you can. You have access to the following tools:
    be sure to minimize the use of tavily as it is expensive to use

    {tools}

            Use the following format:

            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question

            Begin!

            Question: {input}
            Thought:{agent_scratchpad}
"""
prompt = PromptTemplate.from_template(template)
llm = GoogleGenerativeAI(model="models/gemini-1.5-pro-latest", temperature=0.5, google_api_key=st.secrets["api_key"], safety_settings={ HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE})
agent = create_react_agent(llm,tools=[tool_med, tool_search], prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=[tool_med, tool_search], verbose=True)

if prompt :=text:
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke(
            {"input": prompt}, {"callbacks": [st_callback]}
        )
        st.write(response["output"])