# 🎬 Video AI Summarizer

An intelligent video analysis platform powered by Google Gemini AI that enables users to chat with videos and extract insights through natural language conversations.


[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Gemini-2.0-purple.svg)](https://deepmind.google/technologies/gemini/)




## 📋 Description

**Video AI Summarizer** is a sophisticated multimodal AI application that bridges the gap between video content and natural language understanding. Built with cutting-edge technologies, this tool transforms how users interact with video content by enabling conversational analysis.

## 🎯 Results

### Application Screenshots
<img width="1919" height="1028" alt="Screenshot 2026-02-03 203712" src="https://github.com/user-attachments/assets/397655e2-9dd3-480c-997d-de84ae25cbf1" />

<img width="1911" height="1029" alt="Screenshot 2026-02-03 203845" src="https://github.com/user-attachments/assets/0297b80a-902c-436b-9c10-e4c218d99002" />



## ✨ Features

- 🔗 **YouTube Integration** - Paste any YouTube URL to analyze videos
- 📁 **File Upload Support** - Upload video files directly from your device
- 💬 **Interactive Chat Interface** - Ask questions and get AI-powered answers
- 🌐 **Web-Enhanced Responses** - Supplementary information from web search
- 🎨 **Beautiful Modern UI** - Gradient purple theme with smooth animations
- 💾 **Chat History** - Maintains conversation context throughout the session


### How It Works

The application leverages multiple advanced technologies working in harmony:

1. **Video Input Processing**
   - Accepts YouTube URLs via `yt-dlp` for seamless downloading
   - Supports direct file uploads in multiple formats (MP4, MOV, AVI, MKV, WEBM)
   - Temporarily stores and processes videos efficiently

2. **AI Analysis Pipeline**
   - Uploads videos to Google's Gemini API for multimodal processing
   - Utilizes Google Gemini 1.5 Flash model for video understanding
   - Processes visual, audio, and contextual information from videos

3. **Intelligent Agent System**
   - Built with the Phidata framework for agent orchestration
   - Integrates DuckDuckGo search for supplementary web research
   - Generates comprehensive, context-aware responses

4. **Interactive Chat Experience**
   - Real-time streaming responses from the AI agent
   - Persistent chat history within each session
   - Ability to ask follow-up questions and maintain context

### Technology Stack

- **Frontend**: Streamlit (Web UI with custom CSS styling)
- **AI Model**: Google Gemini 1.5 Flash (Multimodal understanding)
- **Agent Framework**: Phidata (Agent orchestration and tool integration)
- **Video Processing**: 
  - `yt-dlp` for YouTube video downloads
  - `google-generativeai` for video upload and processing
- **Search Integration**: DuckDuckGo (Web search capabilities)
- **Environment Management**: Python-dotenv for API key security

### Use Cases

- 📚 **Educational Content Analysis** - Summarize lectures and tutorials
- 🎥 **Content Creation** - Extract key points from research videos
- 📊 **Meeting Analysis** - Get insights from recorded meetings
- 🎬 **Media Research** - Analyze video content for research purposes
- 🔍 **Quick Information Retrieval** - Ask specific questions about video content

## 🚀 Installation

### Prerequisites

- Python 3.12 or higher
- Google Gemini API key
- UV package manager (optional but recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Video Summarizer"
   ```

2. **Install dependencies**
   ```bash
   # Using UV (recommended)
   uv pip install -r requirements.txt
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
   
   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage

1. **Load a Video**
   - Choose between YouTube Link or Upload Video tabs
   - For YouTube: Paste the URL and click "Load YouTube Video"
   - For Upload: Select a file and click "Upload Video"

2. **Wait for Processing**
   - The video will be downloaded/uploaded and processed
   - This may take a few moments depending on video size

3. **Start Chatting**
   - Once loaded, the video player will appear
   - Type your questions in the chat input at the bottom
   - Ask about content, summaries, specific details, or analysis

4. **Manage Your Session**
   - View chat history as you interact
   - Use "Clear Conversation" to reset the chat
   - Use "Reset & Load New Video" to analyze a different video

## 📂 Project Structure

```
Video Summarizer/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

## 🔧 Configuration

### API Requirements

- **Google Gemini API**: Required for video analysis and AI responses
- **Internet Connection**: Needed for YouTube downloads and web search

### Supported Video Formats

- MP4
- MOV
- AVI
- MKV
- WEBM

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Google Gemini for powerful multimodal AI capabilities
- Phidata for the agent framework
- Streamlit for the amazing web framework
- yt-dlp for robust YouTube video downloading

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ using Streamlit and Google Gemini**
