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
                ('OpenChat-7B',))
    with col2:
        start_bot_button = st.button("start bot")
    with col3:
        stop_bot_button = st.button("stop bot")
    
    if start_bot_button:
        user_session_status["bot_status"] = True
        json.dump(user_session_status, open("chat_history.json", "w"))
    if stop_bot_button:
        user_session_status["bot_status"] = False
        json.dump(user_session_status, open("chat_history.json", "w"))
    
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
    # Dashboard stuff (graph, etc put here) Tab 1

    #tab1.title("Control Panel")
    # Bot Status Control Panel

    # Generate new chatbot token
    #change_token_button = tab1.button("Generate new token")
    #if change_token_button:
    #    bot_token = set_bot_token(DASHBOARD_TOKEN)
    #
    ## Show chatbot token
    #bot_token = get_bot_token(DASHBOARD_TOKEN)
    #tab1.write('Chatbot Token: ' + bot_token)

    #col1, col2 = tab1.columns(2)

    # Col 1, turn off bot button
    #with col1:
    #    bot_stop_button = st.button("stop bot")
    #    if bot_stop_button:
    #        tab1.session_state.stop_bot = "true"
    #        # Call the API to stop the Bot Activity and refresh
    #        #bot_status = set_bot_off(os.getenv('CHATBOT_TOKEN'))
    #    
    #    bot_start_button = st.button("start bot")
    #    if bot_start_button:
    #        tab1.session_state.stop_bot = "false"
    #        # Call the API to stop the Bot Activity and refresh
    #        #bot_status = set_bot_on(os.getenv('CHATBOT_TOKEN'))
    #
    ## Col 2, bot status
    ##with col2:
    #    # Call API for Bot Status
    #    #bot_status = get_bot_status()
#
    #    # Display the bot status
    #    #display_status(bot_status)
    #    
    #
    ## Set max chat size
    ##chat_size = get_chat_size()
    ##chat_size_setting = tab1.number_input("Chat Limit", key="chat_limit", value=chat_size, min_value=5, max_value=100, step=1)
#
    ##if chat_size_setting:
    #    # Update the API for change in chat size and then refresh the page
    ##    chat_size = set_chat_size(DASHBOARD_TOKEN, chat_size_setting)
#
    #tab2.title("Chatbot Panel")
    ## Control panel to adjust the bot prompt and temperature
#
#
    ## Prompt
    ##current_prompt = read_system_prompt(JSON_DATABASE_URL) # Call API for current prompt
    ##input_prompt = tab2.text_area(label="Chatbot Prompt:",value=current_prompt)
#
    ## Create a button to update the prompt
    #if tab2.button("Update System Prompt"):
    #    #write_system_prompt(input_prompt, JSON_DATABASE_URL)
    #    tab2.success("Prompt updated!")
#
    ## Fetch the current chat parameters from the API
    ##current_temperature, current_max_token = get_chat_parameter(DASHBOARD_TOKEN)
#
    ## Set the model temperature
    ##temperature = tab2.slider(
    ##    ':blue[Temperature]',
    ##    0.0, 2.0, current_temperature)
    #    
    ## Set the model max token to be generated
    ##max_length = tab2.slider(
    ##    ":blue[Maximum lenght]",
    ##    0, 4096, current_max_token
    ##)
#
    ## Button to update the chat parameters
    ##if tab2.button("Update Chat Parameters"):
    ##    updated_temperature, updated_max_token = set_chat_parameter(temperature, max_length, DASHBOARD_TOKEN)
    ##    if updated_temperature == temperature and updated_max_token == max_length:
    ##        st.success("Chat parameters updated successfully!")
    ##    else:
    ##        st.error("Failed to update chat parameters.")