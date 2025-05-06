import asyncio
import random

import nest_asyncio
import streamlit as st
from agent import ask, create_history
from client import connect_to_server
from config import Config
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from models import create_llm
from tools import load_tools

LOADING_MESSAGES = [
    "Organizing your tasks...",
    "Prioritizing your day...",
    "Consulting my digital checklist...",
    "Processing your request...",
    "Boosting your productivity...",
    "Analyzing your to do list...",
    "Scheduling your success...",
    "Making sense of the task chaos...",
    "Getting your ducks (or tasks) in a row...",
    "Calculating the optimal plan...",
    "Tackling your task list...",
    "Brewing a potion of productivity...",
    "Streamlining your workflow...",
    "Checking things off the list...",
    "Thinking about your next steps...",
]


async def get_response_async(user_query: str, history: list[BaseMessage], llm: BaseChatModel) -> str:
    async with connect_to_server() as session:
        tools = await load_tools(session)
        llm_with_tools = llm.bind_tools(tools)
        response_content = await ask(user_query, history.copy(), llm_with_tools, tools)  # type: ignore
        return response_content


nest_asyncio.apply()

st.set_page_config(
    page_title="DoItR",
    page_icon="✅",
    layout="centered",
)

st.title("ToDo list")
st.subheader("Your AI-powered ToDo assistant")

if "llm" not in st.session_state:
    st.session_state.llm = create_llm(Config.MODEL)

if "messages" not in st.session_state:
    st.session_state.messages = create_history()

for message in st.session_state.messages:
    if type(message) is SystemMessage:
        continue
    is_user = type(message) is HumanMessage
    avatar = "👨‍🦳" if is_user else "🤖"
    with st.chat_message("user" if is_user else "ai", avatar=avatar):
        st.markdown(message.content)

if prompt := st.chat_input("What cat I help you with?"):
    st.session_state.messages.append(HumanMessage(prompt))
    with st.chat_message("human", avatar="👨‍🦳"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.status(random.choice(LOADING_MESSAGES), state="running")

        response = asyncio.run(get_response_async(prompt, st.session_state.messages, st.session_state.llm))

        message_placeholder.markdown(response)
        st.session_state.messages.append(AIMessage(response))
