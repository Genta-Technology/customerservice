import json
import streamlit as st
from datetime import datetime

def chats_page():
    """
    Main chat menu
    """
    st.title('Genta Telegram Chats Page')    
    st.write('Welcome to the chats page!')
    refresh_button = st.button("refresh")
    if "data" not in st.session_state or refresh_button:
        st.session_state["data"] = json.load(open("chat_history.json"))["data"]
    
    st.session_state["data"] = sorted(st.session_state["data"], key=lambda d: d['time_last_conversation'])[::-1]
    chat_index = 0
    for d in st.session_state.data:
        chat_index += 1
        
        with st.expander("Chat " + str(chat_index)):
            chat_col1, chat_col2 = st.columns(2)
            with chat_col1:
            
                # print chat id
                st.write("Chat ID: "+ str(d["chat_id"]))
                
                # print time of last response
                st.write("Last response: "+
                         datetime.utcfromtimestamp(d["time_last_conversation"]).strftime('%Y-%m-%d %H:%M:%S'))
            
            #with chat_col2:
                # delete button and edit button 
                #del_button = st.button("delete last response", key="del_last_msg/id="+d["chat_id"])
                #edit_button = st.button("edit last response", key="edit_msg/id="+d["chat_id"])
            
            # check if the last message is assistant role
            #if del_button and d["chat_history"][-1]["role"] == "assistant":
            #    # remove the last message
            #    st.session_state["del_last_msg"+d["chat_id"]] = True
            #    d["chat_history"] = d["chat_history"][:-1]
            
            # render the chats
            for chats in d["chat_history"]:
                with st.chat_message(chats["role"]):
                    st.write(chats["content"])