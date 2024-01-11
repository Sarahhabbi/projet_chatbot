from openai import OpenAI
import streamlit as st

def initialize_session_state():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

def ask_openai(question, role="user"):
    st.session_state.messages.append({"role": role, "content": question})

    with st.chat_message(role):
        st.markdown(question)

def get_openai_response():
    message_placeholder = st.empty()
    full_response = ""
    for response in client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    ):
        full_response += (response.choices[0].delta.content or "")
        message_placeholder.markdown(full_response + "▌")

    message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

st.title("Welcome to ChatLingo your best friend to practice any language! 😁")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
initialize_session_state()

# show history of messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# button to suggest topics
origin_language = st.selectbox("Select your native language:", ["English", "French", "Spanish", "Chinese"])
language = st.text_input("Enter the language you want topics in:")

if st.button("Suggest some topics"):
    if language.strip() and origin_language.strip():
        # send to open AI API
        question = f"Can you suggest some topics for {language} conversation practice? Answer in {language} and limit to 5 topics. Translate instructions to {origin_language}."
        ask_openai(question, role="user")
        ask_openai("", role="assistant")
        get_openai_response()
    else:
        st.warning("Please enter a valid language.")

# user questions
prompt = st.chat_input("Ask me anything here.")
if prompt:
    ask_openai(prompt, role="user")
    ask_openai("", role="assistant")
    get_openai_response()
