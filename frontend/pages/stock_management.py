import streamlit as st
from utils.api_client import api_client
from utils.auth import check_auth, show_logout_button

# Check authentication first
check_auth()

# Show logout button in sidebar
show_logout_button()

# Helper function to round numbers to 1 decimal place
def round_number(value):
    """Round number to 1 decimal place, handling None values"""
    if value is None:
        return 0.0
    return round(float(value), 1)

st.set_page_config(
    page_title="Stock Management - Stocker",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Stock Management")

# Items section
categories = api_client.get_categories()
items = api_client.get_items()
st.subheader("Items")
if items:
    st.subheader("Current Stock Levels")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Stock Overview", "📝 Log Stock Counts"])
    
    with tab1:
        # Display all items in a table
        for category in categories:
            st.subheader(category.get('name', 'Unknown'))
            for item in items:
                if item.get('category_id') == category.get('id'):
                    quantity = round_number(item.get('quantity', 0))
                    unit = item.get('unit', '')
                    with st.expander(f"{item.get('name', 'Unknown')} - {quantity} {unit}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**Category:** {item.get('category_name', 'Unknown')}")
                        
                        with col2:
                            st.write(f"**Current Stock:** {quantity} {unit}")
                        
                        with col3:
                            threshold = round_number(item.get('restock_threshold', 0))
                            current = round_number(item.get('quantity', 0))
                            if current <= threshold:
                                st.error(f"⚠️ Low Stock (Threshold: {threshold})")
                            else:
                                st.success(f"✅ Good Stock (Threshold: {threshold})")
    
    with tab2:
        st.write("**Log Stock Counts:**")
        
        # Select item to log stock for
        item_names = [item.get('name', 'Unknown') for item in items]
        selected_item_name = st.selectbox("Select Item:", item_names)
        
        if selected_item_name:
            selected_item = next((item for item in items if item.get('name') == selected_item_name), None)
            
            if selected_item:
                current_quantity = round_number(selected_item.get('quantity', 0))
                unit = selected_item.get('unit', '')
                st.write(f"**Current Stock:** {current_quantity} {unit}")
                
                with st.form(f"log_stock_{selected_item.get('id')}"):
                    new_quantity = st.number_input(
                        "New Quantity", 
                        value=current_quantity, 
                        min_value=0.0,
                        step=0.1,
                        key=f"qty_{selected_item.get('id')}"
                    )
                    notes = st.text_input("Notes (optional)", key=f"notes_{selected_item.get('id')}")
                    staff_name = st.text_input("Staff Name (optional)", key=f"staff_name_{selected_item.get('id')}")
                    
                    if st.form_submit_button("Log Stock Count"):
                        result = api_client.log_stock(selected_item.get('id'), round_number(new_quantity), notes, staff_name)
                        if result:
                            st.success("Stock count logged successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to log stock count. Please try again.")

else:
    st.info("No items found. Create some items first!")
    
    # Quick action to go back to main page
    if st.button("🏠 Back to Dashboard"):
        st.switch_page("main.py") 