import streamlit as st


def login_panel():
    st.title("TMS Backend Demo Login")
    st.caption("Use the demo credentials from the README.")
    with st.form("login"):
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
    if submitted:
        if user == "admin" and password == "demo123":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid credentials")
