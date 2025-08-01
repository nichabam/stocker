import streamlit as st
from datetime import datetime
from utils.api_client import api_client
from modules.sidebar import sidebar

# Sidebar
sidebar()

# Page configuration
st.set_page_config(
    page_title="Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main dashboard page
st.title("☕ Stocker")
st.markdown("---")

# Get real data from API
items = api_client.get_items()
categories = api_client.get_categories()
stock_records = api_client.get_stock_records()
restock_records = api_client.get_restock_records()

# Quick stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_items = len(items) if items else 0
    st.metric("Total Items", total_items)

with col2:
    low_stock_items = 0
    if items:
        low_stock_items = len([
            item for item in items 
            if item.get('quantity', 0) <= item.get('restock_threshold', 0)
        ])
    st.metric("Low Stock Items", low_stock_items)

with col3:
    total_categories = len(categories) if categories else 0
    st.metric("Categories", total_categories)

with col4:
    today_restocks = 0
    if restock_records:
        today_restocks = len([
            r for r in restock_records 
            if r.get('date', '').startswith(str(datetime.now().date()))
        ])
    st.metric("Today's Restocks", today_restocks)

# Recent activity
st.subheader("Recent Activity")
if stock_records:
    st.write("Recent stock counts:")
    for record in stock_records[:5]:  # Show last 5
        st.write(f"- {record.get('item_name', 'Unknown')}: {record.get('quantity', 0)} on {record.get('date', 'Unknown')}")
else:
    st.info("No stock records found. Start by logging some stock counts!")
