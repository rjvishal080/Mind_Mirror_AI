import streamlit as st
from dotenv import load_dotenv
from config import initialize_app
from ui_components import setup_custom_styles, setup_sidebar, load_avatars
from chat_page import render_chat_page
from mood_tracker import render_mood_tracker
from journal_page import render_journal_page
from progress_page import render_progress_page
from voice_analytics import render_voice_analytics

def main():
    """Main application function"""
    # Load environment variables and initialize app
    load_dotenv()
    
    # Initialize app configuration
    initialize_app()
    
    # Setup custom styles
    setup_custom_styles()
    
    # Load avatars
    load_avatars()
    
    # Setup sidebar and get navigation choice
    choice = setup_sidebar()
    
    # Route to appropriate page
    if choice == "Chat":
        render_chat_page()
    elif choice == "Mood Tracker":
        render_mood_tracker()
    elif choice == "Journal":
        render_journal_page()
    elif choice == "Progress":
        render_progress_page()
    elif choice == "Voice Analytics":
        render_voice_analytics()

if __name__ == "__main__":
    main()