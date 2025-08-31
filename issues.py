import streamlit as st
import datetime
import json
import os

def render_issues_page():
    """Render the issues and support page"""
    st.title("🐛 Issues & Support")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["🐛 Report Issue", "💡 Feature Request", "📋 Known Issues", "ℹ️ System Info"])
    
    with tab1:
        render_bug_report()
    
    with tab2:
        render_feature_request()
    
    with tab3:
        render_known_issues()
    
    with tab4:
        render_system_info()

def render_bug_report():
    """Render bug report form"""
    st.markdown("### 🐛 Report a Bug")
    st.write("Found a problem? Help us fix it by providing details below.")
    
    with st.form("bug_report_form"):
        # Bug details
        bug_title = st.text_input("🏷️ Bug Title", placeholder="Brief description of the issue")
        
        bug_type = st.selectbox("🔍 Issue Type", [
            "App Crash",
            "Feature Not Working",
            "Voice Issues",
            "API Connection Error",
            "UI/Display Problem",
            "Performance Issue",
            "Other"
        ])
        
        severity = st.selectbox("⚠️ Severity", [
            "Low - Minor inconvenience",
            "Medium - Affects functionality",
            "High - Blocks main features",
            "Critical - App unusable"
        ])
        
        bug_description = st.text_area(
            "📝 Detailed Description", 
            placeholder="Describe what happened, what you expected, and steps to reproduce the issue...",
            height=150
        )
        
        steps_to_reproduce = st.text_area(
            "🔄 Steps to Reproduce",
            placeholder="1. Go to...\n2. Click on...\n3. See error...",
            height=100
        )
        
        environment_info = st.text_area(
            "💻 Environment (Optional)",
            placeholder="Browser, OS, Python version, etc.",
            height=80
        )
        
        # Contact info (optional)
        contact_email = st.text_input("📧 Email (Optional)", placeholder="your.email@example.com")
        
        submitted = st.form_submit_button("🚀 Submit Bug Report")
        
        if submitted and bug_title and bug_description:
            save_issue_report("bug", {
                "title": bug_title,
                "type": bug_type,
                "severity": severity,
                "description": bug_description,
                "steps": steps_to_reproduce,
                "environment": environment_info,
                "contact": contact_email,
                "timestamp": datetime.datetime.now().isoformat()
            })
            st.success("✅ Bug report submitted! Thank you for helping improve Mind Mirror.")
        elif submitted:
            st.error("❌ Please fill in at least the title and description.")

def render_feature_request():
    """Render feature request form"""
    st.markdown("### 💡 Request a Feature")
    st.write("Have an idea to make Mind Mirror better? Share it with us!")
    
    with st.form("feature_request_form"):
        feature_title = st.text_input("🏷️ Feature Title", placeholder="What feature would you like?")
        
        feature_category = st.selectbox("📂 Category", [
            "Chat & AI",
            "Voice & Audio",
            "Mood Tracking",
            "Journal",
            "Analytics",
            "UI/UX",
            "Language Support",
            "Integration",
            "Other"
        ])
        
        priority = st.selectbox("⭐ Priority", [
            "Nice to have",
            "Would be helpful",
            "Important",
            "Critical need"
        ])
        
        feature_description = st.text_area(
            "📝 Feature Description",
            placeholder="Describe the feature you'd like to see. What problem would it solve? How should it work?",
            height=150
        )
        
        use_case = st.text_area(
            "🎯 Use Case",
            placeholder="When and why would you use this feature? Provide specific examples...",
            height=100
        )
        
        contact_email = st.text_input("📧 Email (Optional)", placeholder="your.email@example.com")
        
        submitted = st.form_submit_button("🚀 Submit Feature Request")
        
        if submitted and feature_title and feature_description:
            save_issue_report("feature", {
                "title": feature_title,
                "category": feature_category,
                "priority": priority,
                "description": feature_description,
                "use_case": use_case,
                "contact": contact_email,
                "timestamp": datetime.datetime.now().isoformat()
            })
            st.success("✅ Feature request submitted! We'll consider it for future updates.")
        elif submitted:
            st.error("❌ Please fill in at least the title and description.")

def render_known_issues():
    """Display known issues and their status"""
    st.markdown("### 📋 Known Issues")
    
    known_issues = [
        {
            "title": "Voice input may not work on all browsers",
            "status": "🔍 Investigating",
            "description": "Some browsers may not support voice input due to security restrictions.",
            "workaround": "Try using Chrome or Edge for best voice support."
        },
        {
            "title": "Chat history may reset on browser refresh",
            "status": "🛠️ In Progress", 
            "description": "Browser storage limitations may cause chat history loss.",
            "workaround": "Export important conversations before closing the app."
        },
        {
            "title": "Large chat histories may slow performance",
            "status": "📝 Planned",
            "description": "Very long conversations may cause the app to respond slowly.",
            "workaround": "Clear chat history periodically for better performance."
        },
        {
            "title": "Voice features require microphone permissions",
            "status": "📚 Documentation",
            "description": "First-time users need to grant microphone access.",
            "workaround": "Allow microphone access when prompted by your browser."
        }
    ]
    
    for issue in known_issues:
        with st.expander(f"{issue['status']} {issue['title']}"):
            st.write(f"**Description:** {issue['description']}")
            st.write(f"**Workaround:** {issue['workaround']}")

def render_system_info():
    """Display system and app information"""
    st.markdown("### ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📱 App Info")
        st.write(f"**Version:** 1.0.0")
        st.write(f"**Framework:** Streamlit")
        st.write(f"**AI Model:** Groq Llama3-70B")
        
        # Session state info
        st.markdown("#### 🔧 Session State")
        st.write(f"**Voice Mode:** {'✅ Enabled' if st.session_state.get('voice_mode', False) else '❌ Disabled'}")
        st.write(f"**TTS Enabled:** {'✅ Yes' if st.session_state.get('tts_enabled', True) else '❌ No'}")
        st.write(f"**Language:** {st.session_state.get('language', 'english').title()}")
        st.write(f"**Chat Messages:** {len(st.session_state.get('chat_history', []))}")
        st.write(f"**Mood Entries:** {len(st.session_state.get('mood_history', []))}")
    
    with col2:
        st.markdown("#### 🌐 Environment")
        st.write(f"**API Key Status:** {'✅ Configured' if os.getenv('GROQ_API_KEY') else '❌ Missing'}")
        
        # Check file permissions
        files_to_check = ['.env', 'images/logo.png', 'images/user.jpg', 'images/bot.jpg']
        st.markdown("#### 📁 File Status")
        for file_path in files_to_check:
            exists = os.path.exists(file_path)
            status = "✅ Found" if exists else "❌ Missing"
            st.write(f"**{file_path}:** {status}")
    
    # Diagnostic tools
    st.markdown("---")
    st.markdown("#### 🔧 Diagnostic Tools")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("🧪 Test API Connection"):
            test_api_connection()
    
    with col4:
        if st.button("📊 Export Session Data"):
            export_session_data()

def save_issue_report(issue_type, data):
    """Save issue report to local file"""
    # Create issues directory if it doesn't exist
    os.makedirs("user_reports", exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"user_reports/{issue_type}_{timestamp}.json"
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Also save to session state for immediate display
    if "user_reports" not in st.session_state:
        st.session_state.user_reports = []
    
    st.session_state.user_reports.append({
        "type": issue_type,
        "data": data,
        "filename": filename
    })

def test_api_connection():
    """Test the API connection"""
    try:
        from config import initialize_groq_client
        client = initialize_groq_client()
        
        # Test with a simple message
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            temperature=0.1,
            max_tokens=50
        )
        
        if completion.choices[0].message.content:
            st.success("✅ API connection successful!")
        else:
            st.error("❌ API connection failed - no response received")
            
    except Exception as e:
        st.error(f"❌ API connection failed: {str(e)}")

def export_session_data():
    """Export current session data for debugging"""
    session_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "chat_history_length": len(st.session_state.get('chat_history', [])),
        "mood_history_length": len(st.session_state.get('mood_history', [])),
        "voice_mode": st.session_state.get('voice_mode', False),
        "tts_enabled": st.session_state.get('tts_enabled', True),
        "language": st.session_state.get('language', 'english'),
        "last_emotion": st.session_state.get('last_detected_emotion', None)
    }
    
    # Convert to JSON string for download
    json_string = json.dumps(session_data, indent=2)
    
    st.download_button(
        label="💾 Download Session Data",
        data=json_string,
        file_name=f"mind_mirror_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )
    
    st.success("📋 Session data ready for download!")
