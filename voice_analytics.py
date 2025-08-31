import streamlit as st
from chat_memory import get_emotion_summary
from voice_chat_module import record_voice_input, speak_text

def render_voice_analytics():
    """Render the voice analytics page"""
    st.title("🎭 Voice & Emotion Analytics")
    
    # Create two columns for analytics
    col1, col2 = st.columns(2)
    
    with col1:
        display_emotion_analytics()
    
    with col2:
        display_voice_features()

def display_emotion_analytics():
    """Display emotion analysis and statistics"""
    st.markdown("### 📊 Recent Emotion Analysis")
    emotion_summary = get_emotion_summary(7)
    
    if "error" in emotion_summary:
        st.error(emotion_summary["error"])
    elif "message" in emotion_summary:
        st.info(emotion_summary["message"])
    else:
        st.metric("Total Voice Interactions", emotion_summary["total_interactions"])
        st.metric("Most Common Emotion", emotion_summary["most_common"])
        
        st.markdown("#### Emotion Breakdown")
        for emotion, percentage in emotion_summary["emotion_percentages"].items():
            st.write(f"{emotion}: {percentage}%")

def display_voice_features():
    """Display voice feature testing and settings"""
    st.markdown("### 🎙️ Voice Features")
    
    if st.button("🎤 Test Voice Input"):
        test_input = record_voice_input()
        if test_input:
            st.success(f"Recognized: {test_input}")
    
    if st.button("🔊 Test Voice Output"):
        speak_text("Hello! This is a test of the voice output system. How does this sound?")
        st.success("Voice test completed!")
    
    st.markdown("#### Voice Settings")
    if st.button("🧹 Clear Emotion History"):
        clear_emotion_history()
        st.success("Emotion history cleared!")

def clear_emotion_history():
    """Clear emotion history (placeholder for implementation)"""
    # This would need to be implemented in chat_memory.py
    # For now, it's just a placeholder
    if "emotion_history" in st.session_state:
        st.session_state.emotion_history = []