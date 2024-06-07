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
from langchain_community.utilities import ArxivAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


tool_wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tool_wikidata = WikidataQueryRun(api_wrapper=WikidataAPIWrapper())
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
# TavilySearchAPIWrapper = TavilySearchAPIWrapper(tavily_api_key=st.secrets["TAVILY_API_KEY"])
tool_med = PubmedQueryRun()
tool_search = TavilySearchResults()
tool_arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())


st.title("Medical Help Chatbot")


text = st.chat_input(placeholder="Type your message here...")
# template = template = """
# Answer the following questions as best you can. You are a very helpful medically oriented assistant.
# If the action does not yield the desired result, you can always try another action or the same action with different input. But always give a final answer. Feel free to cross reference with other tools after you check pubmed if needed, but minimize use of tavily as it costs financial resources.

# Use the following format:

# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of the tools you have access to
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat 5 times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question

# Begin!

# Question: {input}
# Thought:{agent_scratchpad}
# """
# prompt = PromptTemplate.from_template(template)

prompt = prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful medical assistant, who will try your best to deliver accurate and helpful information to the user. You have access to the following tools: Pubmed, Tavily Search, Wikipedia, and Wikidata. You can use these tools to help answer the user's questions. Prefer pubmed over tavily search, and minimize tavily search usage as it costs financial resources. You can cross reference with other tools after you check pubmed if needed. Make sure to cite your sources and provide an in depth analysis of the user's question. You will not get stuck when answering a question, which you tended to do before you recieved your MD. You will always give a final answer. If the action does not yield the desired result, you can always try another action or the same action with different input. For Example Arxiv and Pubmed are both excellent sources for scientific papers.",
        ),
        ("placeholder", "{history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
tools = [tool_med, tool_search, tool_wikipedia, tool_wikidata, tool_arxiv]
# prompt.format(tools=tools, tool_names=[tool.name for tool in tools])
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.5, google_api_key=st.secrets["api_key"], safety_settings={ HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE})
# llm.bind_tools(tools)
agent = create_tool_calling_agent(llm,tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


history = StreamlitChatMessageHistory(key="chat_messages") # add user id as key
if len(history.messages) == 0:
    history.add_ai_message("Hello 👋, Welcome to Med Q&A, please note that this is not intended to provide medical advice and merely exists as a small research aid.")

for msg in history.messages:
    st.chat_message(msg.type).write(msg.content)
    
if prompt :=text:
    with st.chat_message("user"):
        st.write(prompt)
        history.add_user_message(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke({"input": prompt, "history": history.messages}, {"callbacks": [st_callback]})
        st.write(response["output"])
        history.add_ai_message(response["output"])
