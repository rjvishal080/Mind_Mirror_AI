import requests
import random

def get_free_ai_response(user_input, chat_history):
    """Free AI response using Hugging Face API (fallback)"""
    try:
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        conversation = "You are a supportive therapist.\n"
        for role, msg in chat_history[-3:]:
            if role == "user":
                conversation += f"User: {msg}\n"
            else:
                conversation += f"Therapist: {msg}\n"
        conversation += f"User: {user_input}\nTherapist:"
        
        payload = {"inputs": conversation, "parameters": {"max_length": 100, "temperature": 0.7}}
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated = result[0].get("generated_text", "")
                if "Therapist:" in generated:
                    bot_response = generated.split("Therapist:")[-1].strip()
                    if bot_response and len(bot_response) > 5:
                        return bot_response
        
        # Return fallback response if API fails
        return get_fallback_response()
        
    except Exception as e:
        return "I'm here to listen and support you. Sometimes I have technical difficulties, but your wellbeing is important to me. What's on your mind?"

def get_fallback_response():
    """Get a random fallback response for when AI APIs fail"""
    fallback_responses = [
        "I understand. That sounds like it must be difficult for you. Can you tell me more about how this makes you feel?",
        "Thank you for sharing that with me. Your feelings are completely valid. What support do you need right now?",
        "I hear you, and I want you to know that it's okay to feel this way. What would be most helpful for you today?",
        "That sounds challenging. You're being very brave by talking about this. How are you coping with these feelings?",
        "I appreciate you opening up to me. It takes courage to share personal experiences. What are your thoughts about this situation?"
    ]
    
    return random.choice(fallback_responses)