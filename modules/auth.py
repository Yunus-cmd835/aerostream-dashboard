import streamlit as st

def login():
    st.sidebar.title("🔐 Login")
    role = st.sidebar.selectbox("Select Role", ["Viewer", "Operator", "Admin"])
    st.session_state.role = role
    st.sidebar.success(f"Logged in as: {role}")
    return role

def has_permission(required_role):
    roles = ["Viewer", "Operator", "Admin"]
    user_role = st.session_state.get("role", "Viewer")
    return roles.index(user_role) >= roles.index(required_role)