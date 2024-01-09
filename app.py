# from openai import OpenAI
# import streamlit as st

# st.title("Welcome to ChatLingo your bestfriend to practice any language !😁")

# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
        
# language = st.text_input("Enter the language you want topics in:")

# # Button to suggest topics
# if st.button("Suggest some topics"):
#     if language.strip():
#         # Send a system message with the question to the OpenAI API
#         question = f"Can you suggest some topics for {language} conversation practice?"
#         st.session_state.messages.append({"role": "user", "content": question + f" answer in {language} and limit to 5 topics"})
#         st.session_state.messages.append({"role": "assistant", "content": ""})

#         with st.chat_message("user"):
#             st.markdown(question)

#         with st.chat_message("assistant"):
#             message_placeholder = st.empty()
#             full_response = ""
#             for response in client.chat.completions.create(
#                 model=st.session_state["openai_model"],
#                 messages=[
#                     {"role": m["role"], "content": m["content"]}
#                     for m in st.session_state.messages
#                 ],
#                 stream=True,
#             ):
#                 full_response += (response.choices[0].delta.content or "")
#                 message_placeholder.markdown(full_response + "▌")
#             message_placeholder.markdown(full_response)
#         st.session_state.messages.append({"role": "assistant", "content": full_response})
 
# prompt = st.chat_input("?")
# if prompt:
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         for response in client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         ):
#             full_response += (response.choices[0].delta.content or "")
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#     st.session_state.messages.append({"role": "assistant", "content": full_response})

from openai import OpenAI
import streamlit as st

def initialize_session_state():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "response_received" not in st.session_state:
        st.session_state.response_received = False

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

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Text input for language
language = st.text_input("Enter the language you want topics in:")

# Button to suggest topics
if st.button("Suggest some topics"):
    if language.strip():
        # Send a system message with the question to the OpenAI API
        question = f"Can you suggest some topics for {language} conversation practice?"
        ask_openai(question + f" Answer in {language} and limit to 5 topics", role="user")
        ask_openai("", role="assistant")
        get_openai_response()
        st.session_state.response_received = True
    else:
        st.warning("Please enter a valid language.")
        st.session_state.response_received = False

# User input
prompt = st.chat_input("Ask me anything here.")
if prompt:
    ask_openai(prompt, role="user")
    ask_openai("", role="assistant")
    get_openai_response()
