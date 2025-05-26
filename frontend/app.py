import sys
import os
import logging
from typing import AsyncIterator

from agents import (Runner, set_default_openai_key, trace)
from openai.types.responses import ResponseTextDeltaEvent
import streamlit as st

from backend import lichtblick_agent

# ====================
# Setup logging
# ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("Lichtblick")

# ============================
# Core async function
# ============================
async def llm_response(api_key: str, message: str) -> AsyncIterator[str]:
    """
    Streams the response from the Lichtblick assistant as an async text generator.

    Args:
        api_key (str): The OpenAI API key to authenticate requests.
        message (str): The user's input message to be processed by the agent.

    Yields:
        str: Incremental chunks of the assistant's response text as they are streamed.
    """
    set_default_openai_key(api_key)
    if not api_key or not api_key.startswith("sk-"):
        logger.error("Missing or invalid OpenAI API key.")
        yield "🤖 API key is missing or invalid. Please check your .env file."
        return

    # Construct context from message history
    context = ""
    for msg in st.session_state.messages[-5:]:  # Use last 5 turns
        role = "User" if msg["role"] == "user" else "Assistant"
        content = msg["content"]
        context += f"{role}: {content}\n\n"  # Double newline for clarity
    context += f"User: {message}"

    try:
        result = Runner.run_streamed(lichtblick_agent, input=message)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                if event.data.delta:
                    yield event.data.delta
        logger.info("Agent streaming complete.")
    except Exception as e:
        logger.exception("Error during agent processing.")
        yield "🤖 Sorry, something went wrong. Please try again."

# ============================
# Lichtblick Streamlit App
# ============================
st.set_page_config(
    page_title="Lichtblick", 
    page_icon="🇩🇪📚", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Sidebar
with st.sidebar:
    st.image("assets/lichtblick_mascot.png")
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

    # ✅ Show "ready" toast only once per session
    if openai_api_key and openai_api_key.startswith("sk-"):
        if not st.session_state.get("api_key_validated"):
            st.toast("💡 Lichtblick is ready!", icon="✅")
            st.session_state.api_key_validated = True
    elif openai_api_key:
        st.toast("❌ Invalid API key format.", icon="⚠️")
        st.session_state.api_key_validated = False

    # Clear chat + reset session
    # 🧹 Centered Clear Chat Button in the sidebar
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.api_key_validated = False
        st.toast("🧹 Chat history cleared!", icon="✅")
    st.markdown("</div>", unsafe_allow_html=True)


# App title
st.title("💡:blue[_Lichtblick_] :orange[_Assistant_]💡")

# Short Description
with st.expander("ℹ️ What is Lichtblick?"):
    st.markdown("Lichtblick is your smart and supportive assistant for learning German through sentence analysis, vocabulary help, and clear explanations.")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("Ready to learn German? Ask me anything!"):
    if not openai_api_key or not openai_api_key.startswith("sk-"):
        st.toast("❌ Please enter a valid OpenAI API key.", icon="⚠️")
        st.stop()

    elif user_input.strip() == "":
        st.toast("⚠️ Please enter a message.", icon="⚠️")

    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user", avatar="🤵🏻"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🤖"):
            try:
                with st.spinner("💬 Lichtblick is thinking..."):
                    with trace("Lichtblick workflow"):
                        response = st.write_stream(llm_response(api_key=openai_api_key, message=user_input))
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                logger.exception("Exception in response streaming.")
                st.toast("🤖 Oops! Something went wrong while processing your request.", icon="❌")
