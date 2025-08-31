import streamlit as st
import speech_recognition as sr
import pyttsx3
import tempfile
import os
import io
from pydub import AudioSegment
from pydub.playback import play
import threading
import time
import queue
import numpy as np
from datetime import datetime
import re

# Initialize global variables
recognizer = sr.Recognizer()
tts_engine = None
audio_queue = queue.Queue()

def initialize_tts():
    """Initialize text-to-speech engine with Tamil support"""
    global tts_engine
    try:
        tts_engine = pyttsx3.init()
        
        # Get available voices
        voices = tts_engine.getProperty('voices')
        
        # Try to find Tamil or Indian English voice
        tamil_voice = None
        indian_voice = None
        
        for voice in voices:
            voice_name = voice.name.lower()
            if 'tamil' in voice_name or 'ta' in voice.id.lower():
                tamil_voice = voice.id
                break
            elif 'india' in voice_name or 'indian' in voice_name:
                indian_voice = voice.id
        
        # Set voice preference: Tamil > Indian English > Default
        if tamil_voice:
            tts_engine.setProperty('voice', tamil_voice)
        elif indian_voice:
            tts_engine.setProperty('voice', indian_voice)
        
        # Set speech rate and volume
        tts_engine.setProperty('rate', 150)  # Slower for better understanding
        tts_engine.setProperty('volume', 0.8)
        
        return True
        
    except Exception as e:
        st.error(f"TTS initialization failed: {e}")
        return False

def detect_language(text):
    """Simple language detection for Tamil vs English"""
    # Tamil Unicode range
    tamil_pattern = re.compile(r'[\u0B80-\u0BFF]')
    
    if tamil_pattern.search(text):
        return 'tamil'
    else:
        return 'english'

def get_voice_input_with_emotion(language_code="ta-IN", timeout=10):
    """
    Enhanced voice input with emotion detection and Tamil support
    """
    try:
        # Initialize recognizer with better settings
        recognizer.energy_threshold = 4000
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 1.0
        
        with sr.Microphone() as source:
            st.info("🎤 Listening... Please speak now!")
            
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Create a placeholder for real-time feedback
            status_placeholder = st.empty()
            
            try:
                # Listen for audio with timeout
                status_placeholder.info("🔴 Recording...")
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
                status_placeholder.info("🔄 Processing...")
                
                # Try Google Speech Recognition first
                try:
                    text = recognizer.recognize_google(
                        audio, 
                        language=language_code,
                        show_all=False
                    )
                    
                    if text:
                        status_placeholder.success(f"✅ Recognized: {text}")
                        
                        # Detect emotion from voice (simplified)
                        emotion = detect_emotion_from_text(text)
                        
                        # Save emotion data
                        save_emotion_data(emotion, datetime.now())
                        
                        # Store in session state
                        st.session_state.last_detected_emotion = emotion
                        
                        return text, emotion
                    
                except sr.UnknownValueError:
                    # Try with alternative language if primary fails
                    alt_lang = "en-IN" if language_code == "ta-IN" else "ta-IN"
                    try:
                        text = recognizer.recognize_google(audio, language=alt_lang)
                        if text:
                            status_placeholder.success(f"✅ Recognized ({alt_lang}): {text}")
                            emotion = detect_emotion_from_text(text)
                            return text, emotion
                    except:
                        pass
                
                except sr.RequestError as e:
                    status_placeholder.error(f"❌ Speech recognition error: {e}")
                
            except sr.WaitTimeoutError:
                status_placeholder.warning("⏰ No speech detected. Please try again.")
                
    except Exception as e:
        st.error(f"Voice input error: {e}")
    
    return None, None

def detect_emotion_from_text(text):
    """
    Simple emotion detection from text (supports Tamil and English)
    """
    text_lower = text.lower()
    
    # Tamil emotion keywords
    tamil_emotions = {
        'happy': ['மகிழ்ச்சி', 'சந்தோஷம்', 'खुशी', 'நல்லா', 'சூப்பர்'],
        'sad': ['வருத்தம்', 'சோகம்', 'दुःख', 'கஷ்டம்', 'அழுகை'],
        'angry': ['கோபம்', 'எரிச்சல்', 'गुस्सा', 'திட்டு'],
        'anxious': ['பதற்றம்', 'டென்ஷன்', 'चिंता', 'பயம்'],
        'excited': ['உத்साகம்', 'ஆர்வம்', 'उत्साह', 'என்னா', 'வாவ்']
    }
    
    # English emotion keywords
    english_emotions = {
        'happy': ['happy', 'joy', 'glad', 'excited', 'good', 'great', 'wonderful', 'awesome'],
        'sad': ['sad', 'depressed', 'down', 'upset', 'hurt', 'disappointed', 'crying'],
        'angry': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'irritated'],
        'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'tense', 'afraid', 'scared'],
        'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil']
    }
    
    # Check Tamil emotions
    for emotion, keywords in tamil_emotions.items():
        for keyword in keywords:
            if keyword in text_lower:
                return emotion
    
    # Check English emotions
    for emotion, keywords in english_emotions.items():
        for keyword in keywords:
            if keyword in text_lower:
                return emotion
    
    return 'neutral'

from gtts import gTTS

def speak_text(text, emotion=None, language=None):
    """
    Speak text using gTTS for Tamil and pyttsx3 for English
    """
    global tts_engine

    if not language:
        language = detect_language(text)

    if language == 'tamil':
        try:
            tts = gTTS(text=text, lang='ta')
            with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
                tts.save(fp.name)
                audio = AudioSegment.from_mp3(fp.name)
                play(audio)
        except Exception as e:
            st.error(f"🔇 Tamil speech error: {e}")
    else:
        # English voice using pyttsx3
        if not tts_engine:
            if not initialize_tts():
                st.error("Text-to-speech not available")
                return

        try:
            # Adjust voice properties based on emotion
            if emotion:
                if emotion == 'happy':
                    tts_engine.setProperty('rate', 180)
                    tts_engine.setProperty('volume', 0.9)
                elif emotion == 'sad':
                    tts_engine.setProperty('rate', 120)
                    tts_engine.setProperty('volume', 0.7)
                elif emotion == 'angry':
                    tts_engine.setProperty('rate', 160)
                    tts_engine.setProperty('volume', 0.8)
                elif emotion == 'anxious':
                    tts_engine.setProperty('rate', 140)
                    tts_engine.setProperty('volume', 0.6)
                else:
                    tts_engine.setProperty('rate', 150)
                    tts_engine.setProperty('volume', 0.8)

            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            st.error(f"🔇 English speech error: {e}")

def create_audio_controls():
    """
    Create audio control interface
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎤 Start Recording"):
            return "record"
    
    with col2:
        if st.button("⏹️ Stop Recording"):
            return "stop"
    
    with col3:
        if st.button("🔊 Test Speaker"):
            return "test_speaker"
    
    return None

def record_voice_input(language_code=None):
    if not language_code:
        language_code = st.session_state.get("language_code", "en-IN")    
    
    if st.button("🎤 Click to Record Voice"):
        with st.spinner("🎙️ Recording... Speak now!"):
            text, emotion = get_voice_input_with_emotion(language_code)
            
            if text:
                st.success(f"✅ Recognized: {text}")
                if emotion and emotion != 'neutral':
                    st.info(f"😊 Detected emotion: {emotion}")
                return text
            else:
                st.error("❌ Could not recognize speech. Please try again.")
                return None
    
    return None

def save_emotion_data(emotion, timestamp):
    """
    Save emotion data to session state and file
    """
    if "emotion_history" not in st.session_state:
        st.session_state.emotion_history = []
    
    emotion_entry = {
        "emotion": emotion,
        "timestamp": timestamp,
        "date": timestamp.date()
    }
    
    st.session_state.emotion_history.append(emotion_entry)
    
    # Keep only last 100 entries to manage memory
    if len(st.session_state.emotion_history) > 100:
        st.session_state.emotion_history = st.session_state.emotion_history[-100:]

def get_emotion_summary(days=7):
    """
    Get emotion summary for specified number of days
    """
    if "emotion_history" not in st.session_state:
        return {"message": "No emotion data available"}
    
    from datetime import datetime, timedelta
    
    # Filter last N days
    cutoff_date = datetime.now().date() - timedelta(days=days)
    recent_emotions = [
        entry for entry in st.session_state.emotion_history 
        if entry["date"] >= cutoff_date
    ]
    
    if not recent_emotions:
        return {"message": f"No emotion data from last {days} days"}
    
    # Calculate statistics
    emotion_counts = {}
    for entry in recent_emotions:
        emotion = entry["emotion"]
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    total = len(recent_emotions)
    most_common = max(emotion_counts, key=emotion_counts.get)
    
    # Calculate percentages
    emotion_percentages = {
        emotion: round((count / total) * 100, 1)
        for emotion, count in emotion_counts.items()
    }
    
    return {
        "total_interactions": total,
        "most_common": most_common,
        "emotion_counts": emotion_counts,
        "emotion_percentages": emotion_percentages
    }

# Test functions
def test_voice_recognition():
    """Test voice recognition functionality"""
    st.write("### 🧪 Voice Recognition Test")
    
    if st.button("Test Tamil Voice Input"):
        text, emotion = get_voice_input_with_emotion("ta-IN")
        if text:
            st.success(f"Tamil Recognition: {text}")
            st.info(f"Emotion: {emotion}")
    
    if st.button("Test English Voice Input"):
        text, emotion = get_voice_input_with_emotion("en-IN")
        if text:
            st.success(f"English Recognition: {text}")
            st.info(f"Emotion: {emotion}")

def test_voice_output():
    """Test voice output functionality"""
    st.write("### 🔊 Voice Output Test")
    
    test_texts = {
        "English": "Hello! This is a test of the English voice system.",
        "Tamil": "வணக்கம்! இது தமிழ் குரல் அமைப்பின் சோதனை."
    }
    
    for lang, text in test_texts.items():
        if st.button(f"Test {lang} Voice"):
            speak_text(text)
            st.success(f"{lang} voice test completed!")

# Export main functions for use in main app
__all__ = [
    'get_voice_input_with_emotion',
    'speak_text',
    'create_audio_controls',
    'record_voice_input',
    'save_emotion_data',
    'get_emotion_summary',
    'initialize_tts',
    'test_voice_recognition',
    'test_voice_output'
]