from monitoring_system.chats import chats_page
from monitoring_system.dashboard import dashboard_page

import streamlit as st 
from PIL import Image

# Genta Logo
logo = Image.open("genta_logo.png")

st.sidebar.title('Navigation')
page = st.sidebar.radio('Menu', ['Dashboard', 'Chat'],
                        label_visibility="hidden")

if page == 'Dashboard':
    dashboard_page()
elif page == 'Chat':
    chats_page()