"""
Streamlit-based Dashboard for AI Customer Service Monitoring.

This module implements a dashboard using Streamlit for monitoring and managing
an AI customer service system. It provides real-time oversight and interaction
capabilities for chat service administrators and managers.

Features:
- Chat Monitoring: View live customer-AI interactions for quality assurance.
- Message Management: Delete or modify messages for error correction.
- Analytics Dashboard: Access usage patterns and performance metrics.
- Secure Login: Restrict dashboard access to authorized personnel.

Getting Started:
To run the dashboard, ensure Streamlit is installed and execute:
`streamlit run dashboard.py`
Login is required for access.

Prerequisites:
- Python 3.x
- Streamlit
- Dependencies listed in requirements.txt

Note:
Ensure API communication with the intended website and LangChain for RAG
(Retrieval-Augmented Generation) are properly configured for seamless integration.
"""
import streamlit as st
import json

from dotenv import load_dotenv

load_dotenv() 

def dashboard_page():
    # load user current data
    user_session_status = json.load(open("chat_history.json"))

    """
    Main dashboard page
    """
    #st.set_page_config(page_icon="./genta_logo.png")
    st.title('Dashboard')
    st.write('Welcome to the telegram dashboard!')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        model_option = st.selectbox(
                'Select Model',
                ('OpenChat-7B','Starstreak'))
    with col2:
        start_bot_button = st.button("start bot")
        stop_bot_button = st.button("stop bot")
    
    if start_bot_button:
        user_session_status["bot_status"] = True
        json.dump(user_session_status, open("chat_history.json", "w"))
    if stop_bot_button:
        user_session_status["bot_status"] = False
        json.dump(user_session_status, open("chat_history.json", "w"))
    with col3:
        st.write("Chatbot API status: ", ":green[ON]" if user_session_status["bot_status"] else ":red[OFF]")
    
    genta_token = st.text_input("genta token", user_session_status["genta_token"])
    telegram_token = st.text_input("telegram bot token",user_session_status["telegram_bot_token"])
    prompt = st.text_input("prompt", value=user_session_status["prompt"])
    #genta_token = st.text_input("genta token")
    chat_size_setting = st.number_input("Chat Limit", key="chat_limit", value=user_session_status["max_chat_size"], min_value=5, max_value=100, step=1)
    #tab1, tab2 = st.tabs(["Control Panel", "Chatbot Panel"])
    temperature = st.slider(
            ':blue[Temperature]',
            0.0, 2.0, user_session_status["temperature"])
            
    # Set the model max token to be generated
    max_length = st.slider(
        ":blue[Maximum length]",
        0, 4096, user_session_status["max_token"]
    )
    update_user_session = st.button("update parameters")
    if update_user_session:
        user_session_status["model_selection"] = model_option
        user_session_status["genta_token"] = genta_token
        user_session_status["telegram_bot_token"] = telegram_token
        user_session_status["prompt"] = prompt
        user_session_status["max_chat_size"] = chat_size_setting
        user_session_status["max_token"] = max_length
        user_session_status["temperature"] = temperature
        json.dump(user_session_status, open("chat_history.json", "w"))