import streamlit as st

def toast_success(msg: str):
    st.markdown(f"""<div class="toast success">{msg}</div>""", unsafe_allow_html=True)

def toast_warn(msg: str):
    st.markdown(f"""<div class="toast warn">{msg}</div>""", unsafe_allow_html=True)
