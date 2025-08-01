import streamlit as st
import requests
from datetime import datetime
from utils.api_client import api_client

# Page configuration
st.set_page_config(
    page_title="Stocker - Cafe Inventory Management",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_BASE_URL = "http://localhost:8000"

def main():
    st.title("☕ Stocker - Cafe Inventory Management")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Dashboard", "Stock Management", "Restock Logging", "Analytics"]
    )
    
    # Main content area
    if page == "Dashboard":
        show_dashboard()
    elif page == "Stock Management":
        show_stock_management()
    elif page == "Restock Logging":
        show_restock_logging()
    elif page == "Analytics":
        show_analytics()

def show_dashboard():
    st.header("📊 Dashboard")
    
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

def show_stock_management():
    st.header("📦 Stock Management")
    
    # Get items from API
    items = api_client.get_items()
    
    if items:
        st.subheader("Current Stock Levels")
        for item in items:
            with st.expander(f"{item.get('name', 'Unknown')} - {item.get('quantity', 0)} {item.get('unit', '')}"):
                st.write(f"**Category:** {item.get('category_name', 'Unknown')}")
                st.write(f"**Restock Threshold:** {item.get('restock_threshold', 0)} {item.get('unit', '')}")
                
                # Log stock count form
                with st.form(f"log_stock_{item.get('id')}"):
                    new_quantity = st.number_input("New Quantity", value=float(item.get('quantity', 0)), key=f"qty_{item.get('id')}")
                    notes = st.text_input("Notes (optional)", key=f"notes_{item.get('id')}")
                    if st.form_submit_button("Log Stock Count"):
                        result = api_client.log_stock(item.get('id'), new_quantity, notes)
                        if result:
                            st.success("Stock count logged successfully!")
                            st.rerun()
    else:
        st.info("No items found. Create some items first!")

def show_restock_logging():
    st.header("📥 Restock Logging")
    st.info("Restock logging features coming soon...")

def show_analytics():
    st.header("📈 Analytics")
    st.info("Analytics features coming soon...")

if __name__ == "__main__":
    main()
