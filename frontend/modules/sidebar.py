import streamlit as st

def sidebar():
    with st.sidebar:
        st.page_link("main.py", label="Dashboard")
        st.sidebar.divider()
        st.page_link("pages/stock_management.py", label="Stock Management", icon="📦")
        st.page_link("pages/category_management.py", label="Categories")
        st.page_link("pages/item_management.py", label="Items")
