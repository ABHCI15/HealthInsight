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
from langchain_community.tools.wikidata.tool import WikidataAPIWrapper, WikidataQueryRun
import os 
from langchain.agents import create_tool_calling_agent
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

tool_wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tool_wikidata = WikidataQueryRun(api_wrapper=WikidataAPIWrapper())
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
# TavilySearchAPIWrapper = TavilySearchAPIWrapper(tavily_api_key=st.secrets["TAVILY_API_KEY"])
tool_med = PubmedQueryRun()
tool_search = TavilySearchResults()



st.title("Medical Help Chatbot")

with st.chat_message("assistant"):
    st.write("Hello 👋, Welcome to Med Q&A, please note that this is not intended to provide medical advice and merely exists as a small research aid.")

text = st.chat_input(placeholder="Type your message here...")
template = template = """
Answer the following questions as best you can. You are a very helpful medically oriented assistant.
If the action does not yield the desired result, you can always try another action or the same action with different input. But always give a final answer. Feel free to cross reference with other tools after you check pubmed if needed, but minimize use of tavily as it costs financial resources.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of the tools you have access to
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat 5 times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
prompt = PromptTemplate.from_template(template)
tools = [tool_med, tool_search, tool_wikipedia, tool_wikidata]
# prompt.format(tools=tools, tool_names=[tool.name for tool in tools])
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.5, google_api_key=st.secrets["api_key"], safety_settings={ HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE})
# llm.bind_tools(tools)
agent = create_tool_calling_agent(llm,tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


history = StreamlitChatMessageHistory(key="chat_messages") # add user id as key

if prompt :=text:
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        out = agent_executor.invoke({"input": prompt})
        print(out)
        st.markdown(f"```{out}```")
