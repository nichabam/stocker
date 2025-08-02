import streamlit as st
import hashlib

# Simple authentication for single cafe
CAFE_USERNAME = "cafe"
CAFE_PASSWORD = "stock2024"  # You can change this

def hash_password(password: str) -> str:
    """Hash password for comparison"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username: str, password: str) -> bool:
    """Check if username and password match"""
    return username == CAFE_USERNAME and password == CAFE_PASSWORD

def login_page():
    """Display login page"""
    st.title("☕ Stocker - Login")
    st.markdown("---")
    
    # Login form
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        if st.form_submit_button("Login"):
            if check_credentials(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    # Show credentials for easy access
    with st.expander("ℹ️ Login Credentials"):
        st.write(f"**Username:** {CAFE_USERNAME}")
        st.write(f"**Password:** {CAFE_PASSWORD}")
        st.info("These credentials are for cafe staff use only.")

def check_auth():
    """Check if user is authenticated, redirect to login if not"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        login_page()
        st.stop()
    
    return True

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()

def show_logout_button():
    """Show logout button in sidebar"""
    if st.session_state.get('authenticated', False):
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout"):
            logout() 