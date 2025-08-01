import streamlit as st
from utils.api_client import api_client
from modules.sidebar import sidebar

# Sidebar
sidebar()

st.set_page_config(
    page_title="Item Management - Stocker",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Item Management")

# Get existing data
items = api_client.get_items()
categories = api_client.get_categories()

# Create tabs for different operations
tab1, tab2, tab3 = st.tabs(["📋 View Items", "➕ Create Item", "✏️ Edit Items"])

with tab1:
    st.subheader("All Items")
    
    if items:
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            show_low_stock = st.checkbox("Show only low stock items", value=False)
        with col2:
            category_filter = st.selectbox(
                "Filter by category:",
                options=["All Categories"] + [cat.get('name', 'Unknown') for cat in (categories or [])]
            )
        
        # Filter items
        filtered_items = items
        if show_low_stock:
            filtered_items = [item for item in items if item.get('quantity', 0) <= item.get('restock_threshold', 0)]
        if category_filter != "All Categories":
            filtered_items = [item for item in filtered_items if item.get('category_name') == category_filter]
        
        # Display items
        for item in filtered_items:
            with st.expander(f"📦 {item.get('name', 'Unknown')} - {item.get('quantity', 0)} {item.get('unit', '')}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Name:** {item.get('name', 'Unknown')}")
                    st.write(f"**Category:** {item.get('category_name', 'Unknown')}")
                    st.write(f"**Unit:** {item.get('unit', 'Unknown')}")
                
                with col2:
                    current_stock = item.get('quantity', 0)
                    threshold = item.get('restock_threshold', 0)
                    
                    if current_stock <= threshold:
                        st.error(f"⚠️ Low Stock ({current_stock}/{threshold})")
                    else:
                        st.success(f"✅ Good Stock ({current_stock}/{threshold})")
                
                with col3:
                    st.write(f"**ID:** {item.get('id', 'Unknown')}")
                    # Delete button
                    if st.button("🗑️ Delete", key=f"delete_item_{item.get('id')}"):
                        result = api_client.delete_item(item.get('id'))
                        if result:
                            st.success("✅ Item deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete item. Please try again.")
    else:
        st.info("No items found. Create your first item in the 'Create Item' tab!")

with tab2:
    st.subheader("Create New Item")
    
    if categories:
        with st.form("create_item_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                item_name = st.text_input("Item Name", placeholder="e.g., Coffee Beans, Milk, Sugar")
                unit = st.text_input("Unit", placeholder="e.g., kg, L, pieces")
                restock_threshold = st.number_input("Restock Threshold", min_value=0.0, value=5.0, step=0.1)
            
            with col2:
                # Category selection
                category_options = {cat.get('name', 'Unknown'): cat.get('id') for cat in categories}
                selected_category_name = st.selectbox("Category:", options=list(category_options.keys()))
                selected_category_id = category_options[selected_category_name]
                
                # Preview
                st.write("**Preview:**")
                st.write(f"Name: {item_name}")
                st.write(f"Unit: {unit}")
                st.write(f"Threshold: {restock_threshold}")
                st.write(f"Category: {selected_category_name}")
            
            if st.form_submit_button("Create Item"):
                if item_name.strip() and unit.strip():
                    result = api_client.create_item(
                        name=item_name.strip(),
                        unit=unit.strip(),
                        restock_threshold=restock_threshold,
                        category_id=selected_category_id
                    )
                    if result:
                        st.success(f"✅ Item '{item_name}' created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to create item. Please try again.")
                else:
                    st.error("❌ Item name and unit are required!")
    else:
        st.warning("⚠️ No categories found. Please create categories first!")
        if st.button("📂 Go to Category Management"):
            st.switch_page("pages/category_management.py")

with tab3:
    st.subheader("Edit Items")
    
    if items:
        selected_item_name = st.selectbox(
            "Select Item to Edit:",
            options=[item.get('name', 'Unknown') for item in items],
            key="edit_item_select"
        )
        
        if selected_item_name:
            item_to_edit = next((item for item in items if item.get('name') == selected_item_name), None)
            
            if item_to_edit:
                st.write(f"**Editing:** {item_to_edit.get('name')}")
                
                with st.form("edit_item_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("New Name", value=item_to_edit.get('name', ''))
                        new_unit = st.text_input("New Unit", value=item_to_edit.get('unit', ''))
                        new_threshold = st.number_input("New Threshold", min_value=0.0, value=float(item_to_edit.get('restock_threshold', 0)), step=0.1)
                    
                    with col2:
                        # Category selection for edit
                        if categories:
                            category_options = {cat.get('name', 'Unknown'): cat.get('id') for cat in categories}
                            current_category = item_to_edit.get('category_name', 'Unknown')
                            new_category_name = st.selectbox("New Category:", options=list(category_options.keys()), index=list(category_options.keys()).index(current_category) if current_category in category_options else 0)
                            new_category_id = category_options[new_category_name]
                        else:
                            new_category_id = item_to_edit.get('category_id')
                            st.write("No categories available")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.form_submit_button("Update Item"):
                            result = api_client.update_item(
                                item_to_edit.get('id'),
                                name=new_name.strip(),
                                unit=new_unit.strip(),
                                restock_threshold=new_threshold,
                                category_id=new_category_id
                            )
                            if result:
                                st.success("✅ Item updated successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update item. Please try again.")
                    
                    with col2:
                        if st.form_submit_button("Delete Item"):
                            result = api_client.delete_item(item_to_edit.get('id'))
                            if result:
                                st.success("✅ Item deleted successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete item. Please try again.")
    else:
        st.info("No items to edit. Create some items first!")

# Quick navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Back to Dashboard"):
        st.switch_page("main.py")
with col2:
    if st.button("📂 Category Management"):
        st.switch_page("pages/category_management.py")
