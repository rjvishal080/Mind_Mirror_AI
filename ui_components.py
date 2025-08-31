import streamlit as st
import base64
from chat_memory import clear_chat_history

def setup_custom_styles():
    """Setup custom CSS styles for the application"""
    st.markdown("""
        <style>
            .chat-message {
                display: flex;
                align-items: flex-start;
                gap: 0.75rem;
                margin-bottom: 1.2rem;
            }
            .chat-message.user {
                flex-direction: row-reverse;
            }
            .chat-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
            }
            .chat-name {
                font-size: 0.9rem;
                color: #666;
                font-weight: 600;
                margin-bottom: 4px;
            }
            .chat-bubble {
                margin: 0;
                padding: 1rem 1.2rem;
                border-radius: 16px;
                max-width: 85%;
                white-space: pre-wrap;
                font-size: 1rem;
                line-height: 1.5;
                font-weight: 600;
            }
            .chat-bubble.user {
                background-color: #D0E8FF;
                color: #003366;
                border-bottom-right-radius: 4px;
            }
            .chat-bubble.assistant {
                background-color: #F4E1FF;
                color: #4B006E;
                border-bottom-left-radius: 4px;
            }
            .voice-indicator {
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                color: white;
                font-weight: bold;
                margin: 10px 0;
            }
            .emotion-badge {
                display: inline-block;
                background-color: #f0f2f6;
                color: #333;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8rem;
                margin-left: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def image_to_base64(image_path):
    """Convert image to base64 with error handling"""
    try:
        with open(image_path, "rb") as f:
            data = f.read()
            return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"
    except FileNotFoundError:
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMjAiIGZpbGw9IiM2NjY2NjYiLz4KPC9zdmc+"

def load_avatars():
    """Load and store avatars in session state"""
    if "user_avatar" not in st.session_state:
        st.session_state.user_avatar = image_to_base64("images/user.jpg")
    if "bot_avatar" not in st.session_state:
        st.session_state.bot_avatar = image_to_base64("images/bot.jpg")

def setup_sidebar():
    """Setup sidebar navigation and settings"""
    with st.sidebar:
        # Logo
        try:
            st.image("images/logo.png", width=150)
        except:
            st.write("🧠 Mind Mirror")
        
        # Language selection
        language = st.selectbox("🗣️ Select Language", ["English", "Tamil"], index=0)
        
        # Set language settings
        if language == "English":
            language_code = "en-IN"
            session_lang = "english"
        else:
            language_code = "ta-IN"
            session_lang = "tamil"
        
        # Store in session_state
        st.session_state.language_code = language_code
        st.session_state.language = session_lang
        
        # Navigation
        choice = st.radio("Navigate", ["Chat", "Mood Tracker", "Journal", "Progress", "Voice Analytics"])
        
        st.markdown("---")
        st.markdown("### 🎙️ Voice Settings")
        
        # Voice settings
        voice_mode = st.checkbox("🗣️ Voice Mode", value=st.session_state.voice_mode)
        st.session_state.voice_mode = voice_mode
        
        tts_enabled = st.checkbox("🔊 Voice Responses", value=st.session_state.tts_enabled)
        st.session_state.tts_enabled = tts_enabled
        
        # Emotion display
        if st.session_state.last_detected_emotion:
            st.info(f"Last emotion: {st.session_state.last_detected_emotion}")
        
        # Clear chat history
        if st.button("🧹 Clear Chat History"):
            clear_chat_history()
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
    
    return choice