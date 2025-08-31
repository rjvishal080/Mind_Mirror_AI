import streamlit as st
import datetime
from voice_chat_module import record_voice_input

def render_mood_tracker():
    """Render the mood tracker page"""
    st.title("😊 Enhanced Mood Tracker")
    
    moods = ["😊 Happy", "😐 Okay", "😔 Sad", "😠 Angry", "😰 Anxious", "😴 Tired", "😍 Loved"]
    
    st.write("How are you feeling right now?")
    
    # Voice mood input
    if st.button("🎤 Tell me how you feel"):
        voice_mood = record_voice_input()
        if voice_mood:
            st.write(f"You said: {voice_mood}")
            # Simple mood detection from text
            mood_detected = detect_mood_from_text(voice_mood, moods)
            
            if mood_detected:
                st.success(f"Detected mood: {mood_detected}")
                save_mood_entry(mood_detected, "voice")
            else:
                st.info("Couldn't detect a specific mood, but your input was recorded.")

    # Manual mood selection
    selected_mood = st.selectbox("Or select your mood:", moods)
    
    if st.button("Save Mood"):
        save_mood_entry(selected_mood, "manual")
        st.success(f"Mood {selected_mood} saved!")

    # Display mood history
    display_mood_history()

def detect_mood_from_text(text, moods):
    """Detect mood from voice text input"""
    mood_detected = None
    for mood in moods:
        mood_word = mood.split()[1].lower()
        if mood_word in text.lower():
            mood_detected = mood
            break
    return mood_detected

def save_mood_entry(mood, method):
    """Save a mood entry to session state"""
    st.session_state.mood_history.append({
        "mood": mood,
        "timestamp": datetime.datetime.now(),
        "method": method
    })

def display_mood_history():
    """Display recent mood history"""
    if st.session_state.mood_history:
        st.markdown("### Recent Moods")
        for entry in st.session_state.mood_history[-5:]:
            method_icon = "🎤" if entry["method"] == "voice" else "📝"
            st.write(f"{method_icon} {entry['mood']} - {entry['timestamp'].strftime('%Y-%m-%d %H:%M')}")