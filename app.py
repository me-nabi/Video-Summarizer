import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import google.generativeai as genai

import time
from pathlib import Path
import tempfile
import yt_dlp
import os
import re

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Multimodal AI Agent - Video Summarizer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Video container styling */
    [data-testid="stVideo"] {
        max-height: 280px;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        border: 2px solid rgba(139, 92, 246, 0.3);
    }
    
    video {
        max-height: 280px !important;
        width: 100% !important;
        margin: 0 auto;
        border-radius: 15px;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background: linear-gradient(145deg, #1e1e1e, #2d2d2d);
        border: 2px solid rgba(139, 92, 246, 0.5);
        border-radius: 12px;
        padding: 12px 20px;
        font-size: 1rem;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
    }
    
    /* Chat message styling */
    [data-testid="stChatMessageContainer"] {
        background: rgba(139, 92, 246, 0.05);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #8b5cf6;
    }
    
    /* User message */
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 18px 18px 5px 18px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }
    
    /* Assistant message */
    .stChatMessage[data-testid="assistant"] {
        background: linear-gradient(145deg, #2d2d2d, #1e1e1e);
        border-radius: 18px 18px 18px 5px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    /* Chat input styling */
    .stChatInput > div > div > input {
        background: linear-gradient(145deg, #2d2d2d, #1e1e1e);
        border: 2px solid rgba(139, 92, 246, 0.5);
        border-radius: 25px;
        padding: 12px 20px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stChatInput > div > div > input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
    }
    
    /* Info box styling */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #8b5cf6;
        background: rgba(139, 92, 246, 0.1);
    }
    
    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    /* Divider styling */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #8b5cf6, transparent);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e1e 0%, #2d2d2d 100%);
        border-right: 2px solid rgba(139, 92, 246, 0.3);
    }
    
    [data-testid="stSidebar"] h2 {
        color: #8b5cf6;
        font-weight: 600;
    }
    
    /* Compact layout */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Subheader styling */
    h3 {
        color: #8b5cf6;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #8b5cf6 transparent transparent transparent;
    }
    
    /* Reduce spacing */
    .stVideo {
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Custom header
st.markdown("""
    <div class="main-header">
        <h1>🎬 Video AI Summarizer</h1>
        <p>✨ Powered by Google Gemini 2.0 | Chat with any YouTube video using AI</p>
    </div>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-3-flash-preview"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL"""
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    return re.match(youtube_regex, url) is not None

def download_youtube_video(url):
    """Download YouTube video and return the file path"""
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"youtube_video_{int(time.time())}.mp4")
    
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return output_path

# Initialize the agent
multimodal_Agent = initialize_agent()

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'processed_video' not in st.session_state:
    st.session_state.processed_video = None
if 'video_path' not in st.session_state:
    st.session_state.video_path = None

# Create tabs for YouTube URL and File Upload
tab1, tab2 = st.tabs(["🔗 YouTube Link", "📁 Upload Video"])

with tab1:
    # YouTube URL input
    youtube_url = st.text_input(
        "Enter YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste a YouTube video link to analyze"
    )

    if st.button("🎬 Load YouTube Video", key="load_youtube_button"):
        if not youtube_url:
            st.warning("Please enter a YouTube URL.")
        elif not is_valid_youtube_url(youtube_url):
            st.error("Please enter a valid YouTube URL.")
        else:
            try:
                with st.spinner("Downloading and processing YouTube video..."):
                    # Download video
                    video_path = download_youtube_video(youtube_url)
                    st.session_state.video_path = video_path
                    
                    # Upload and process video file with Gemini
                    processed_video = upload_file(video_path)
                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)
                    
                    st.session_state.processed_video = processed_video
                    st.session_state.chat_history = []  # Reset chat history for new video
                    st.success("✅ Video loaded successfully! You can now chat with it.")
                    
            except Exception as error:
                st.error(f"An error occurred while loading the video: {error}")

with tab2:
    # File uploader
    video_file = st.file_uploader(
        "Upload a video file",
        type=['mp4', 'mov', 'avi', 'mkv', 'webm'],
        help="Upload a video file from your device"
    )
    
    if st.button("📤 Upload Video", key="upload_video_button"):
        if not video_file:
            st.warning("Please select a video file to upload.")
        else:
            try:
                with st.spinner("Processing uploaded video..."):
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
                        temp_video.write(video_file.read())
                        video_path = temp_video.name
                    
                    st.session_state.video_path = video_path
                    
                    # Upload and process video file with Gemini
                    processed_video = upload_file(video_path)
                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)
                    
                    st.session_state.processed_video = processed_video
                    st.session_state.chat_history = []  # Reset chat history for new video
                    st.success("✅ Video uploaded and loaded successfully! You can now chat with it.")
                    
            except Exception as error:
                st.error(f"An error occurred while uploading the video: {error}")

# Display video if loaded
if st.session_state.video_path and os.path.exists(st.session_state.video_path):
    col1, col2, col3 = st.columns([0.5, 4, 0.5])
    with col2:
        st.video(st.session_state.video_path, format="video/mp4", start_time=0)

# Chat interface
if st.session_state.processed_video:
    st.divider()
    st.subheader("💬 Chat with Video")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, chat in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(chat["question"])
            with st.chat_message("assistant"):
                st.markdown(chat["answer"])
    
    # Chat input
    user_query = st.chat_input("Ask anything about the video...")
    
    if user_query:
        # Add user message to chat history
        with st.chat_message("user"):
            st.write(user_query)
        
        try:
            with st.spinner("Analyzing..."):
                # Prompt generation for analysis
                analysis_prompt = f"""
                Analyze the uploaded video for content and context.
                Respond to the following query using video insights and supplementary web research if needed:
                {user_query}

                Provide a detailed, user-friendly, and actionable response.
                """
                
                # AI agent processing
                response = multimodal_Agent.run(
                    analysis_prompt, 
                    videos=[st.session_state.processed_video]
                )
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(response.content)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": user_query,
                    "answer": response.content
                })
                
        except Exception as error:
            st.error(f"An error occurred during analysis: {error}")
else:
    st.info("👆 Enter a YouTube URL and click 'Load Video' to start chatting with it.")

# Clear conversation button
if st.session_state.chat_history:
    if st.button("🗑️ Clear Conversation", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

# Cleanup on sidebar
with st.sidebar:
    st.markdown("### 📖 About")
    st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; border-left: 3px solid #8b5cf6;'>
            <p style='margin: 0; color: rgba(255,255,255,0.9);'>
                🎥 Upload any YouTube video<br>
                💬 Chat with AI about content<br>
                🔍 Get instant insights<br>
                🌐 Web-powered answers
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🔄 Reset & Load New Video", use_container_width=True):
        # Cleanup old video file
        if st.session_state.video_path and os.path.exists(st.session_state.video_path):
            Path(st.session_state.video_path).unlink(missing_ok=True)
        
        st.session_state.processed_video = None
        st.session_state.video_path = None
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem;'>
            <p>Made with ❤️ using Streamlit</p>
            <p>© 2026 Video AI Summarizer</p>
        </div>
    """, unsafe_allow_html=True)