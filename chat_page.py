import streamlit as st
from config import initialize_groq_client
from chat_memory import load_chat_history, save_chat_history
from voice_chat_module import record_voice_input, speak_text
from ai_responses import get_free_ai_response

def render_chat_page():
    """Render the main chat page"""
    st.title("💬 Mind Mirror Chat")
    
    if st.session_state.voice_mode:
        st.markdown('<div class="voice-indicator">🎙️ Voice Mode Active</div>', unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_chat_history()

    # Voice input section
    if st.session_state.voice_mode:
        spoken_input = record_voice_input()
        if spoken_input:
            st.success(f"🎤 You said: {spoken_input}")
            user_input = spoken_input
        else:
            user_input = None
    else:
        user_input = st.chat_input("Type your message here...")

    # Display chat history
    display_chat_history()
    
    # Process user input
    if user_input:
        process_user_input(user_input)

def display_chat_history():
    """Display the chat history with custom styling"""
    chat_container = st.container()
    
    with chat_container:
        for role, message in st.session_state.chat_history:
            avatar = st.session_state.user_avatar if role == "user" else st.session_state.bot_avatar
            name = "You" if role == "user" else "Therapist"
            bubble_class = "user" if role == "user" else "assistant"
            st.markdown(f"""
            <div class="chat-message {bubble_class}">
                <img src="{avatar}" class="chat-avatar" />
                <div>
                    <div class="chat-name">{name}</div>
                    <div class="chat-bubble {bubble_class}">{message}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def process_user_input(user_input):
    """Process user input and generate AI response"""
    # Add user message to chat history
    st.session_state.chat_history.append(("user", user_input))

    # Build message history for Groq
    messages = [
        {
            "role": "system",
            "content": (
                "You are a kind, empathetic therapist. "
                "Mirror the language and tone of the user: "
                "- If the user writes in English, reply in English.\n"
                "- If the user writes in Tamil, reply in Tamil.\n"
                "- If the user writes in Tanglish (Tamil + English), reply in Tanglish.\n"
                "Your tone should be friendly, supportive, and informal. Do not translate the user's message—respond naturally in the same language or mix used."
                f"The user's current emotional state appears to be: {st.session_state.last_detected_emotion or 'unknown'}. "
                "Please respond with appropriate empathy and support."
            )
        }
    ]

    # Add recent chat history
    for role, msg in st.session_state.chat_history[-10:]:  # Last 10 messages for context
        messages.append({"role": role, "content": msg})

    # Get AI response
    with st.spinner("Therapist is thinking..."):
        try:
            client = initialize_groq_client()
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            reply = completion.choices[0].message.content.strip()

        except Exception as e:
            st.error(f"Groq API Error: {e}")
            reply = get_free_ai_response(user_input, st.session_state.chat_history)

    # Add assistant reply to chat history
    st.session_state.chat_history.append(("assistant", reply))
    
    # Save chat history
    save_chat_history(st.session_state.chat_history)

    # Text-to-speech for bot response
    if st.session_state.tts_enabled:
        with st.spinner("🔊 Speaking response..."):
            speak_text(reply, st.session_state.last_detected_emotion)

    st.rerun()