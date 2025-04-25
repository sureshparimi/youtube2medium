import streamlit as st
from supabase_client import supabase

def login():
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            result = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = result.user
            st.success("Logged in successfully!")
        except Exception as e:
            st.error(f"Login failed: {e}")

def signup():
    st.subheader("📝 Sign Up")
    email = st.text_input("Email (signup)")
    password = st.text_input("Password (signup)", type="password")
    if st.button("Create Account"):
        try:
            result = supabase.auth.sign_up({"email": email, "password": password})
            st.success("Check your email to confirm your account.")
        except Exception as e:
            st.error(f"Signup failed: {e}")