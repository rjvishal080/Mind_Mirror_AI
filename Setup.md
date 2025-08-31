# 🚀 Mind Mirror App - Complete Setup Guide

## 📋 Pre-requisites

- Python 3.8 or higher
- Git (for cloning the repository)
- A Groq API account (free at [console.groq.com](https://console.groq.com/))

## 🛠️ Step-by-Step Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/mind-mirror-app.git
cd mind-mirror-app
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv mind_mirror_env

# Activate virtual environment
# On Windows:
mind_mirror_env\Scripts\activate

# On macOS/Linux:
source mind_mirror_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

#### Method 1: Using .env file (Recommended)
```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your favorite editor
nano .env  # or code .env, vim .env, etc.
```

Replace the placeholder with your actual API key:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

#### Method 2: Environment Variables (Alternative)
```bash
# On Windows (Command Prompt)
set GROQ_API_KEY=gsk_your_actual_groq_api_key_here

# On Windows (PowerShell)
$env:GROQ_API_KEY="gsk_your_actual_groq_api_key_here"

# On macOS/Linux
export GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

### 5. Get Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_`)

### 6. Create Required Directories and Files
```bash
# Create images directory
mkdir images

# You'll need to add these image files:
# - images/logo.png (your app logo)
# - images/user.jpg (user avatar)
# - images/bot.jpg (bot avatar)
```

### 7. Implement Missing Modules

The app requires two additional modules that you need to implement:

#### A. Create `chat_memory.py`
```python
# Basic template for chat_memory.py
import json
import os
from datetime import datetime

def load_chat_history():
    """Load chat history from file"""
    try:
        with open('chat_history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_chat_history(history):
    """Save chat history to file"""
    with open('chat_history.json', 'w') as f:
        json.dump(history, f, indent=2)

def clear_chat_history():
    """Clear chat history"""
    if os.path.exists('chat_history.json'):
        os.remove('chat_history.json')

def save_emotion_data(emotion, timestamp=None):
    """Save emotion data"""
    # Implement emotion tracking
    pass

def get_emotion_summary(days=7):
    """Get emotion summary for specified days"""
    # Implement emotion summary
    return {"message": "No emotion data available"}
```

#### B. Create `voice_chat_module.py`
```python
# Basic template for voice_chat_module.py
import streamlit as st

def get_voice_input_with_emotion():
    """Get voice input with emotion detection"""
    # Implement voice input functionality
    return None, None

def speak_text(text, emotion=None):
    """Convert text to speech"""
    # Implement text-to-speech functionality
    st.info(f"🔊 Speaking: {text}")

def create_audio_controls():
    """Create audio control interface"""
    # Implement audio controls
    pass

def record_voice_input():
    """Record voice input from user"""
    # Implement voice recording
    st.info("🎤 Voice input not implemented yet")
    return None
```

### 8. Run the Application
```bash
streamlit run main.py
```

The app should open in your browser at `http://localhost:8501`

## 🔧 Configuration Options

### Streamlit Configuration
Create `.streamlit/config.toml` for custom Streamlit settings:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
headless = false
port = 8501
```

### Debug Mode
Add to your `.env` file:
```env
DEBUG_MODE=True
LOG_LEVEL=DEBUG
```

## 🎯 Testing Your Setup

1. **Test API Connection**:
   - Go to Chat page
   - Send a message
   - Verify you get a response from Groq

2. **Test Voice Features** (if implemented):
   - Enable voice mode in sidebar
   - Test voice input and output

3. **Test Mood Tracking**:
   - Go to Mood Tracker
   - Select and save a mood
   - Check if it appears in history

## 🚨 Troubleshooting

### Common Issues and Solutions

#### API Key Issues
```
Error: GROQ_API_KEY not configured!
```
**Solution**: Check your `.env` file exists and contains the correct API key.

#### Import Errors
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: 
```bash
pip install -r requirements.txt
```

#### Permission Errors
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: Run with appropriate permissions or check file ownership.

#### Port Already in Use
```
Port 8501 is already in use
```
**Solution**: 
```bash
streamlit run main.py --server.port 8502
```

### Getting Help

1. Check the console output for error messages
2. Verify all files are in the correct locations
3. Ensure your Python version is compatible
4. Check that all dependencies are installed

## 🔒 Security Best Practices

1. **Never commit `.env` files** - They're in `.gitignore`
2. **Use environment variables** for sensitive data
3. **Regularly rotate API keys**
4. **Keep dependencies updated**:
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

## 📦 Deployment Options

### Local Development
- Perfect for testing and development
- Run with `streamlit run main.py`

### Streamlit Cloud
1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in Streamlit Cloud dashboard

### Docker (Optional)
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
```

## 🎉 You're All Set!

Your Mind Mirror app should now be running successfully. Enjoy exploring the features and feel free to customize it further!

For additional support, check the main README.md or create an issue on GitHub.
