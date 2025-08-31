import json
import os
from datetime import datetime, timedelta
import streamlit as st

# File paths for storing data
CHAT_HISTORY_FILE = "data/chat_history.json"
EMOTION_DATA_FILE = "data/emotions.json"
USER_DATA_FILE = "data/user_data.json"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def load_chat_history():
    """Load chat history from file"""
    try:
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('messages', [])
        return []
    except Exception as e:
        st.error(f"Error loading chat history: {e}")
        return []

def save_chat_history(chat_history):
    """Save chat history to file"""
    try:
        data = {
            'messages': chat_history,
            'last_updated': datetime.now().isoformat(),
            'total_messages': len(chat_history)
        }
        
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving chat history: {e}")
        return False

def clear_chat_history():
    """Clear all chat history"""
    try:
        if os.path.exists(CHAT_HISTORY_FILE):
            os.remove(CHAT_HISTORY_FILE)
        
        # Clear from session state
        if "chat_history" in st.session_state:
            st.session_state.chat_history = []
        
        return True
    except Exception as e:
        st.error(f"Error clearing chat history: {e}")
        return False

def save_emotion_data(emotion, timestamp):
    """Save emotion data with timestamp"""
    try:
        # Load existing emotion data
        emotion_data = load_emotion_data()
        
        # Add new emotion entry
        new_entry = {
            'emotion': emotion,
            'timestamp': timestamp.isoformat(),
            'date': timestamp.date().isoformat()
        }
        
        emotion_data.append(new_entry)
        
        # Keep only last 1000 entries to prevent file from getting too large
        if len(emotion_data) > 1000:
            emotion_data = emotion_data[-1000:]
        
        # Save back to file
        with open(EMOTION_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'emotions': emotion_data,
                'last_updated': datetime.now().isoformat(),
                'total_entries': len(emotion_data)
            }, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving emotion data: {e}")
        return False

def load_emotion_data():
    """Load emotion data from file"""
    try:
        if os.path.exists(EMOTION_DATA_FILE):
            with open(EMOTION_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('emotions', [])
        return []
    except Exception as e:
        st.error(f"Error loading emotion data: {e}")
        return []

def get_emotion_summary(days=7):
    """Get emotion summary for the last N days"""
    try:
        emotion_data = load_emotion_data()
        
        if not emotion_data:
            return {"message": "No emotion data available"}
        
        # Filter data for the last N days
        cutoff_date = datetime.now().date() - timedelta(days=days)
        recent_emotions = []
        
        for entry in emotion_data:
            try:
                entry_date = datetime.fromisoformat(entry['date']).date()
                if entry_date >= cutoff_date:
                    recent_emotions.append(entry)
            except (KeyError, ValueError):
                continue
        
        if not recent_emotions:
            return {"message": f"No emotion data from the last {days} days"}
        
        # Calculate statistics
        emotion_counts = {}
        daily_emotions = {}
        
        for entry in recent_emotions:
            emotion = entry['emotion']
            date = entry['date']
            
            # Count emotions
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Group by date
            if date not in daily_emotions:
                daily_emotions[date] = []
            daily_emotions[date].append(emotion)
        
        # Calculate percentages
        total_interactions = len(recent_emotions)
        emotion_percentages = {
            emotion: round((count / total_interactions) * 100, 1)
            for emotion, count in emotion_counts.items()
        }
        
        # Find most common emotion
        most_common = max(emotion_counts, key=emotion_counts.get) if emotion_counts else "None"
        
        return {
            "total_interactions": total_interactions,
            "most_common": most_common,
            "emotion_counts": emotion_counts,
            "emotion_percentages": emotion_percentages,
            "daily_breakdown": daily_emotions,
            "days_analyzed": days
        }
        
    except Exception as e:
        return {"error": f"Error analyzing emotion data: {e}"}

def get_mood_trends(days=30):
    """Get mood trends over time"""
    try:
        emotion_data = load_emotion_data()
        
        if not emotion_data:
            return {"message": "No emotion data available for trend analysis"}
        
        # Filter data for the last N days
        cutoff_date = datetime.now().date() - timedelta(days=days)
        trend_data = {}
        
        for entry in emotion_data:
            try:
                entry_date = datetime.fromisoformat(entry['date']).date()
                if entry_date >= cutoff_date:
                    date_str = entry_date.isoformat()
                    emotion = entry['emotion']
                    
                    if date_str not in trend_data:
                        trend_data[date_str] = {}
                    
                    trend_data[date_str][emotion] = trend_data[date_str].get(emotion, 0) + 1
            except (KeyError, ValueError):
                continue
        
        return {
            "trend_data": trend_data,
            "days_analyzed": days,
            "total_days_with_data": len(trend_data)
        }
        
    except Exception as e:
        return {"error": f"Error analyzing mood trends: {e}"}

def save_user_preferences(preferences):
    """Save user preferences"""
    try:
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'preferences': preferences,
                'last_updated': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving user preferences: {e}")
        return False

def load_user_preferences():
    """Load user preferences"""
    try:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('preferences', {})
        return {}
    except Exception as e:
        st.error(f"Error loading user preferences: {e}")
        return {}

def get_chat_statistics():
    """Get statistics about chat interactions"""
    try:
        chat_history = load_chat_history()
        
        if not chat_history:
            return {"message": "No chat data available"}
        
        # Count messages by role
        user_messages = sum(1 for role, _ in chat_history if role == "user")
        assistant_messages = sum(1 for role, _ in chat_history if role == "assistant")
        
        # Calculate average message length
        user_msg_lengths = [len(msg) for role, msg in chat_history if role == "user"]
        assistant_msg_lengths = [len(msg) for role, msg in chat_history if role == "assistant"]
        
        avg_user_length = sum(user_msg_lengths) / len(user_msg_lengths) if user_msg_lengths else 0
        avg_assistant_length = sum(assistant_msg_lengths) / len(assistant_msg_lengths) if assistant_msg_lengths else 0
        
        return {
            "total_messages": len(chat_history),
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "avg_user_message_length": round(avg_user_length, 1),
            "avg_assistant_message_length": round(avg_assistant_length, 1),
            "conversation_sessions": estimate_sessions(chat_history)
        }
        
    except Exception as e:
        return {"error": f"Error calculating chat statistics: {e}"}

def estimate_sessions(chat_history):
    """Estimate number of conversation sessions based on time gaps"""
    if len(chat_history) < 2:
        return 1 if chat_history else 0
    
    sessions = 1
    session_gap_threshold = timedelta(hours=2)  # Consider > 2 hours gap as new session
    
    # This is a simplified version since we don't have timestamps in the current format
    # In a real implementation, you'd want to store timestamps with messages
    
    return max(1, len(chat_history) // 20)  # Rough estimate: 1 session per ~20 messages

def clear_all_data():
    """Clear all stored data (chat, emotions, preferences)"""
    try:
        files_to_clear = [CHAT_HISTORY_FILE, EMOTION_DATA_FILE, USER_DATA_FILE]
        
        for file_path in files_to_clear:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Clear session state
        session_keys_to_clear = ['chat_history', 'emotion_history', 'mood_history']
        for key in session_keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        return True
        
    except Exception as e:
        st.error(f"Error clearing data: {e}")
        return False

def export_data():
    """Export all user data to a single JSON file"""
    try:
        export_data = {
            'chat_history': load_chat_history(),
            'emotion_data': load_emotion_data(),
            'user_preferences': load_user_preferences(),
            'export_timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        export_filename = f"mind_mirror_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(export_filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return export_filename
        
    except Exception as e:
        st.error(f"Error exporting data: {e}")
        return None

# Helper functions for data validation and migration
def validate_data_integrity():
    """Check data integrity and fix common issues"""
    issues_found = []
    
    try:
        # Check chat history
        chat_history = load_chat_history()
        valid_messages = []
        
        for item in chat_history:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                role, message = item
                if role in ['user', 'assistant'] and isinstance(message, str):
                    valid_messages.append((role, message))
                else:
                    issues_found.append(f"Invalid message format: {item}")
            else:
                issues_found.append(f"Invalid chat entry: {item}")
        
        if len(valid_messages) != len(chat_history):
            save_chat_history(valid_messages)
            issues_found.append("Fixed chat history format issues")
        
        # Check emotion data
        emotion_data = load_emotion_data()
        valid_emotions = []
        
        for entry in emotion_data:
            if isinstance(entry, dict) and 'emotion' in entry:
                valid_emotions.append(entry)
            else:
                issues_found.append(f"Invalid emotion entry: {entry}")
        
        return {
            "issues_found": issues_found,
            "chat_messages": len(valid_messages),
            "emotion_entries": len(valid_emotions)
        }
        
    except Exception as e:
        return {"error": f"Error validating data: {e}"}

# Initialize data structure on import
def initialize_data_structure():
    """Initialize basic data structure if files don't exist"""
    if not os.path.exists(CHAT_HISTORY_FILE):
        save_chat_history([])
    
    if not os.path.exists(EMOTION_DATA_FILE):
        save_emotion_data('neutral', datetime.now())

# Run initialization
initialize_data_structure()