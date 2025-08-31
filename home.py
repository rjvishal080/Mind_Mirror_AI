import streamlit as st

st.set_page_config(page_title="Mind Mirror", layout="centered")

# Display logo (export from Figma as PNG)
st.image("images/logo.png", use_container_width=True)

st.markdown("<h2 style='text-align:center; margin-top:1em;'>Welcome to Mind Mirror</h2>", unsafe_allow_html=True)
st.write("Choose what you'd like to do today:")

# Navigation Buttons
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Mood_Tracker.py", label="🧠 Mood Tracker", icon="🧠")
    st.page_link("pages/2_Journal.py", label="📝 Journal", icon="📝")
with col2:
    st.page_link("pages/3_Chat.py", label="💬 Chat", icon="💬")
    st.page_link("pages/4_Progress.py", label="📊 Progress", icon="📊")
