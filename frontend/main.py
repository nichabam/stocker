import streamlit as st
from datetime import datetime
from utils.api_client import api_client
from utils.auth import check_auth, show_logout_button

# Check authentication first
check_auth()

# Helper function to round numbers to 1 decimal place
def round_number(value):
    """Round number to 1 decimal place, handling None values"""
    if value is None:
        return 0.0
    return round(float(value), 1)

# Page configuration
st.set_page_config(
    page_title="Stocker - Cafe Inventory Management",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show logout button in sidebar
show_logout_button()

# API configuration
API_BASE_URL = "http://localhost:8000"

# Main dashboard page
st.title("☕ Stocker - Cafe Inventory Management")
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
            if round_number(item.get('quantity', 0)) <= round_number(item.get('restock_threshold', 0))
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
        quantity = round_number(record.get('quantity', 0))
        staff_name = record.get('staff_name', 'Unknown')
        item_name = record.get('item_name', 'Unknown')
        date = record.get('date', 'Unknown')
        
        if staff_name and staff_name != 'Unknown':
            st.write(f"- {item_name}: {quantity} (by {staff_name}) on {date}")
        else:
            st.write(f"- {item_name}: {quantity} on {date}")
else:
    st.info("No stock records found. Start by logging some stock counts!")

# Quick actions
# st.subheader("Quick Actions")
# col1, col2 = st.columns(2)

# with col1:
#     if st.button("📦 View Stock Management"):
#         st.switch_page("pages/stock_management.py")

# with col2:
#     if st.button("📥 Log Restock"):
#         st.switch_page("pages/restock_logging.py")
