import streamlit as st

def sidebar():
    with st.sidebar:
        st.page_link("main.py", label="Dashboard")
        st.page_link("pages/stock_management.py", label="Stock Management")
        st.page_link("pages/analytics.py", label="Analytics")
