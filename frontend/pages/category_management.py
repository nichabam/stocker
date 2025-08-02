import streamlit as st
from utils.api_client import api_client
from utils.auth import check_auth, show_logout_button

# Check authentication first
check_auth()

# Show logout button in sidebar
show_logout_button()

st.set_page_config(
    page_title="Category Management - Stocker",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Category Management")

# Get existing categories
categories = api_client.get_categories()

# Create tabs for different operations
tab1, tab2, tab3 = st.tabs(["📋 View Categories", "➕ Create Category", "✏️ Edit Categories"])

with tab1:
    st.subheader("All Categories")
    
    if categories:
        # Display categories in a table format
        for category in categories:
            with st.expander(f"📁 {category.get('name', 'Unknown')}"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Name:** {category.get('name', 'Unknown')}")
                    if category.get('description'):
                        st.write(f"**Description:** {category.get('description', 'No description')}")
                    else:
                        st.write("**Description:** No description")
                
                with col2:
                    st.write(f"**ID:** {category.get('id', 'Unknown')}")
                
                with col3:
                    # Delete button
                    if st.button("🗑️ Delete", key=f"delete_{category.get('id')}"):
                        result = api_client.delete_category(category.get('id'))
                        if result:
                            st.success("✅ Category deleted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete category. Make sure it has no items.")
    else:
        st.info("No categories found. Create your first category in the 'Create Category' tab!")

with tab2:
    st.subheader("Create New Category")
    
    with st.form("create_category_form"):
        category_name = st.text_input("Category Name", placeholder="e.g., Beverages, Dairy, Snacks")
        category_description = st.text_area("Description (optional)", placeholder="Describe what items belong in this category")
        
        if st.form_submit_button("Create Category"):
            if category_name.strip():
                result = api_client.create_category(category_name.strip())
                if result:
                    st.success(f"✅ Category '{category_name}' created successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to create category. Please try again.")
            else:
                st.error("❌ Category name is required!")

with tab3:
    st.subheader("Edit Categories")
    
    if categories:
        selected_category = st.selectbox(
            "Select Category to Edit:",
            options=[cat.get('name', 'Unknown') for cat in categories],
            key="edit_category_select"
        )
        
        if selected_category:
            category_to_edit = next((cat for cat in categories if cat.get('name') == selected_category), None)
            
            if category_to_edit:
                st.write(f"**Editing:** {category_to_edit.get('name')}")
                
                with st.form("edit_category_form"):
                    new_name = st.text_input("New Name", value=category_to_edit.get('name', ''))
                    new_description = st.text_area("New Description", value=category_to_edit.get('description', ''))
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.form_submit_button("Update Category"):
                            result = api_client.update_category(
                                category_to_edit.get('id'),
                                new_name.strip(),
                                new_description.strip() if new_description.strip() else None
                            )
                            if result:
                                st.success("✅ Category updated successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update category. Please try again.")
                    
                    with col2:
                        if st.form_submit_button("Delete Category"):
                            result = api_client.delete_category(category_to_edit.get('id'))
                            if result:
                                st.success("✅ Category deleted successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete category. Make sure it has no items.")
    else:
        st.info("No categories to edit. Create some categories first!")

# Quick navigation
st.markdown("---")
if st.button("🏠 Back to Dashboard"):
    st.switch_page("main.py")
