import streamlit as st
from main import AutoStreamAgent

# Initialize the agent in session state if not already done
if 'agent' not in st.session_state:
    st.session_state.agent = AutoStreamAgent()

if 'messages' not in st.session_state:
    st.session_state.messages = []

st.title("AutoStream AI Chatbot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    response = st.session_state.agent.process_message(prompt)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
