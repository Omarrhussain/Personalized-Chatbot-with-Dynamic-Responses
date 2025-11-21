# 🤖 Personalized RAG Chatbot

A sophisticated Retrieval-Augmented Generation (RAG) chatbot powered by Google Gemini AI, featuring both local and cloud deployment options with FastAPI backend and Streamlit frontend.

## 🚀 Features

- **Dual Deployment**: Run locally with large vector databases or deploy to cloud with optimized small databases
- **RAG Architecture**: Enhanced responses using retrieved context from knowledge base
- **Conversation History**: Maintains context across chat sessions
- **Multiple UI Options**: Streamlit interface for both local and cloud usage
- **RESTful API**: FastAPI backend with comprehensive endpoints

## 🏗️ Project Structure
Personalized_Chatbot/
├── src/
│ ├── MLOps/
│ │ └── api/
│ │ └── app.py # FastAPI application
│ └── model/
│ └── gemini_rag_system.py # RAG system core logic
├── model/
│ ├── gemini-rag/ # Large local vector database
│ └── gemini-rag-small/ # Small cloud-optimized database
├── config/
│ └── api_keys.py # API keys configuration
├── api_server.py # Local API server runner
├── streamlit_app.py # Local Streamlit interface
├── streamlit_cloud.py # Cloud Streamlit interface
├── requirements.txt # Python dependencies
└── railway.json # Railway deployment config

text

## 🛠️ Installation

1. **Clone the repository**
bash
git clone https://github.com/Omarrhussain/Personalized-Chatbot-with-Dynamic-Responses.git
cd Personalized_Chatbot
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Set up API keys

Get Google Gemini API key from Google AI Studio

Add to config/api_keys.py:

python
GEMINI_API_KEY = "your_actual_api_key_here"
🎯 Quick Start
Option 1: Local Development
Start the API server (Terminal 1):

bash
python api_server.py
Launch the Streamlit app (Terminal 2):

bash
streamlit run streamlit_app.py
Access the application:

Streamlit UI: http://localhost:8501

API Docs: http://localhost:8000/docs

Option 2: Cloud Deployment
Deploy to Railway:

Connect your GitHub repo to Railway

Add GEMINI_API_KEY environment variable

Railway automatically deploys on git push

Use cloud Streamlit app:

bash
streamlit run streamlit_cloud.py
📡 API Endpoints
Method	Endpoint	Description
GET	/	API status
GET	/health	Health check
POST	/chat	Send chat message
GET	/conversation/history	Get chat history
DELETE	/conversation/clear	Clear history
Chat Request Example
python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "What is machine learning?",
        "use_history": True
    }
)
🌐 Deployment Guides
Railway Deployment
Fork this repository

Connect to Railway at railway.app

Add GEMINI_API_KEY in Railway variables

Deploy automatically from GitHub

AWS Elastic Beanstalk
Install AWS CLI and EB CLI

Initialize Elastic Beanstalk:

bash
eb init -p python-3.9 personalized-chatbot
eb create production
Deploy:

bash
eb deploy
🔧 Configuration
Vector Databases
Local: model/gemini-rag/ - Full knowledge base (excluded from git)

Cloud: model/gemini-rag-small/ - Optimized for deployment

Environment Variables
GEMINI_API_KEY: Google Gemini API key

PORT: Server port (default: 8000)

📊 Knowledge Base
The RAG system uses a curated knowledge base covering:

Artificial Intelligence & Machine Learning

Deep Learning & Neural Networks

Natural Language Processing

Computer Vision

Reinforcement Learning

And more AI-related topics

🐛 Troubleshooting
Common Issues
API Key Errors

Verify GEMINI_API_KEY is set correctly

Check Google AI Studio for quota limits

Vector Database Not Found

Ensure model/gemini-rag-small/ exists for cloud deployment

Run vector database creation script if missing

Port Conflicts

Change ports in api_server.py and app.py if 8000/8501 are occupied

Import Errors

Verify Python path includes src/ directory

Check all dependencies in requirements.txt

Logs & Debugging
Check Railway logs in deployment dashboard

Use /health and /debug endpoints for status

Enable detailed logging in gemini_rag_system.py

🤝 Contributing
Fork the project

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

Happy Chatting! 🎉
