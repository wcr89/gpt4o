import streamlit as st
import asyncio
from openai import AsyncOpenAI

try:
    client = AsyncOpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = AsyncOpenAI()

# Function to clear chat history
def clear_history():
    st.session_state["messages"] = [{"role": "assistant", "content": "ผมเป็น chatbot ตอบคำถามได้ทุกเรื่อง"}]
    st.experimental_rerun()  # Rerun the script to refresh the page

# Sidebar with OpenAI API key and other links
with st.sidebar:
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password", value=st.secrets.get("OPENAI_API_KEY", ""))
    if st.button("Clear History"):
        clear_history()

st.title("💬 Chatbot GPT4o for Rudy")
st.caption("🚀 A Streamlit chatbot powered by OpenAI model gpt4o")

# Initialize messages if not present in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "ผมเป็น chatbot ตอบคำถามได้ทุกเรื่อง"}
    ]

# Display chat messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Input for new chat messages
if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # client = AsyncOpenAI(api_key=openai_api_key)
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Create an empty container for the assistant's response
    response_container = st.empty()
    assistant_response = ""

    async def generate_response():
        stream = await client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state["messages"],
            stream=True
        )
        streamed_text = ""
        async for chunk in stream:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content is not None:
                streamed_text += chunk_content
                response_container.info(streamed_text)
        st.session_state["messages"].append({"role": "assistant", "content": streamed_text})
        st.chat_message("assistant").write(streamed_text)

    asyncio.run(generate_response())
