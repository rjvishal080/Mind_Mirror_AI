import streamlit as st
import os
from groq import Groq

def initialize_app():
    """Initialize app configuration and API clients"""
    # Page Config
    st.set_page_config(page_title="Mind Mirror App", layout="centered")
    
    # Initialize session state for voice features
    if "tts_enabled" not in st.session_state:
        st.session_state.tts_enabled = True
    if "last_detected_emotion" not in st.session_state:
        st.session_state.last_detected_emotion = None
    if "voice_mode" not in st.session_state:
        st.session_state.voice_mode = False
    if "mood_history" not in st.session_state:
        st.session_state.mood_history = []

def initialize_groq_client():
    """Initialize Groq API client with error handling"""
    # Load Groq API key from .env with error checking
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Check if API key exists
    if not GROQ_API_KEY:
        st.error("⚠️ GROQ_API_KEY not found! Please check your .env file or environment variables.")
        st.stop()
    
    # Initialize Groq client only if API key exists
    try:
        client = Groq(api_key=GROQ_API_KEY)
        return client
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {e}")
        st.stop()

def get_language_settings():
    """Get current language settings from session state"""
    language = st.session_state.get('language', 'english')
    language_code = st.session_state.get('language_code', 'en-IN')
    return language, language_code