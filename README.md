# 🧠 Mind Mirror - AI Therapy Chat App

An empathetic AI-powered therapy chat application built with Streamlit, featuring voice interactions, mood tracking, and multi-language support.

## ✨ Features

- 💬 **AI Therapy Chat** - Empathetic conversations with AI therapist
- 🎤 **Voice Integration** - Voice input and text-to-speech responses
- 😊 **Mood Tracking** - Track and analyze your emotional patterns
- 📝 **Digital Journal** - Voice-to-text journaling capabilities
- 📊 **Progress Analytics** - Visualize your mental health journey
- 🌐 **Multi-language Support** - English and Tamil language support
- 🎭 **Emotion Analysis** - Voice-based emotion detection

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Groq API key (get one free at [console.groq.com](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mind-mirror-app.git
   cd mind-mirror-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your API keys
   nano .env  # or use your preferred editor
   ```

4. **Configure your API key**
   Open `.env` file and replace:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   With your actual Groq API key:
   ```
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```

5. **Create required directories**
   ```bash
   mkdir -p images
   # Add your image files (logo.png, user.jpg, bot.jpg) to the images/ folder
   ```

6. **Run the application**
   ```bash
   streamlit run main.py
   ```

## 📁 Project Structure

```
mind_mirror_app/
├── main.py                 # Main application entry point
├── config.py              # Configuration and API setup
├── ui_components.py       # UI styling and components
├── chat_page.py          # Chat interface
├── mood_tracker.py       # Mood tracking features
├── journal_page.py       # Journal functionality
├── progress_page.py      # Analytics and progress
├── voice_analytics.py    # Voice emotion analysis
├── ai_responses.py       # AI response handling
├── chat_memory.py        # Chat memory management (implement separately)
├── voice_chat_module.py  # Voice processing (implement separately)
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── images/             # Image assets
    ├── logo.png
    ├── user.jpg
    └── bot.jpg
```

## 🔧 Configuration

### API Keys Required
- **Groq API** (Required) - For AI chat responses
- **Hugging Face API** (Optional) - Fallback AI responses

### Environment Variables
Create a `.env` file with the following:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### Additional Setup
You'll need to implement two additional modules:
- `chat_memory.py` - For saving/loading chat history
- `voice_chat_module.py` - For voice input/output functionality

## 🎯 Usage

1. **Chat Mode**: Have conversations with the AI therapist
2. **Voice Mode**: Enable voice input for hands-free interaction  
3. **Mood Tracking**: Log and track your daily moods
4. **Journal**: Write or speak your thoughts and experiences
5. **Analytics**: View your emotional patterns and progress

## 🛡️ Privacy & Security

- No chat data is stored on external servers
- All conversations are processed locally or through secure APIs
- API keys are kept in environment variables (never committed to git)
- User data remains on your local machine

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📋 TODO

- [ ] Implement `chat_memory.py` module
- [ ] Implement `voice_chat_module.py` module  
- [ ] Add data export functionality
- [ ] Implement user authentication
- [ ] Add more language support
- [ ] Create mobile-responsive design
- [ ] Add offline mode capabilities

## 🐛 Troubleshooting

### Common Issues

**API Key Error**
- Ensure your `.env` file exists and contains valid API key
- Check that `.env` is in the root directory
- Verify your Groq API key is active

**Voice Features Not Working**
- Check microphone permissions
- Ensure `voice_chat_module.py` is properly implemented
- Verify audio dependencies are installed

**Import Errors**
- Run `pip install -r requirements.txt`
- Check Python version compatibility
- Ensure all required files are present

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [Groq](https://groq.com/)
- Fallback AI by [Hugging Face](https://huggingface.co/)

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/mind-mirror-app/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**⚠️ Disclaimer**: This application is for educational and wellness purposes only. It is not a substitute for professional mental health care. Please consult qualified healthcare providers for serious mental health concerns.
