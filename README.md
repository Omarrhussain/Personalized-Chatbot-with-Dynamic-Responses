# 🤖 Personalized RAG Chatbot

A powerful Retrieval-Augmented Generation (RAG) chatbot powered by **Google Gemini AI**, supporting both **local** and **cloud** deployment.  
Built using **FastAPI** for the backend and **Streamlit** for the user interface.  
Designed for intelligent, dynamic, and context-aware conversations through vector-based retrieval.

---

## 🚀 Features

- **Dual Deployment Modes**
  - 🖥️ Local deployment with large vector database
  - ☁️ Cloud deployment with optimized small vector database

- **RAG Architecture**
  - Retrieves context from a curated AI and ML knowledge base

- **Conversation Memory**
  - Maintains history across interactions

- **Multiple Frontends**
  - Local Streamlit interface
  - Cloud Streamlit interface

- **RESTful API**
  - Fully documented through FastAPI’s Swagger UI

## 🏗️ Project Structure
```plaintext
Personalized_Chatbot/
├── src/
│   ├── MLOps/
│   │   └── api/
│   │       └── app.py                # FastAPI application
│   └── model/
│       └── gemini_rag_system.py      # RAG system core logic
│
├── model/
│   ├── gemini-rag/                   # Large local vector database
│   └── gemini-rag-small/             # Small cloud-optimized DB
│
├── config/
│   └── api_keys.py                   # API key configuration
│
├── api_server.py                     # Local API server
├── streamlit_app.py                  # Local Streamlit interface
├── streamlit_cloud.py                # Cloud Streamlit interface
├── requirements.txt                  # Python dependencies
└── railway.json                      # Railway deployment config
```



## 🛠️ Installation

1. **Clone the repository**
git clone https://github.com/Omarrhussain/Personalized-Chatbot-with-Dynamic-Responses.git
cd Personalized_Chatbot
Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install dependencies

```bash
pip install -r requirements.txt
```
Set up API keys

Get Google Gemini API key from Google AI Studio

Add to config/api_keys.py:
python
GEMINI_API_KEY = "your_actual_api_key_here"

# 🎯 Quick Start
Option 1: Local Development
Start the API server (Terminal 1):

```bash
python api_server.py
```
Launch the Streamlit app (Terminal 2):

```bash 

streamlit run streamlit_app.py
```
Access the application:
Streamlit UI: http://localhost:8501
API Docs: http://localhost:8000/docs

Option 2: Cloud Deployment

Deploy to Railway:
Connect your GitHub repo to Railway
Add GEMINI_API_KEY environment variable
Railway automatically deploys on git push

Use cloud Streamlit app:

streamlit run streamlit_cloud.py
# 📡 API Endpoints
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

# 🌐 Deployment Guides
Railway Deployment
Fork this repository
Connect to Railway at railway.app
Add GEMINI_API_KEY in Railway variables
Deploy automatically from GitHub
AWS Elastic Beanstalk
Install AWS CLI and EB CLI

Initialize Elastic Beanstalk:
eb init -p python-3.9 personalized-chatbot
eb create production
# Deploy:
eb deploy
# 🔧 Configuration
Vector Databases
Local: model/gemini-rag/ - Full knowledge base (excluded from git)
Cloud: model/gemini-rag-small/ - Optimized for deployment
Environment Variables
GEMINI_API_KEY: Google Gemini API key
PORT: Server port (default: 8000)

# 📊 Knowledge Base
Includes context for diverse AI topics:
- AI & Machine Learning
- Deep Learning
- NLP
- Computer Vision
- Reinforcement Learning
- More advanced AI fields

# 🐛 Troubleshooting
- API Key Errors
- Ensure GEMINI_API_KEY is correctly set
- Check quota in Google AI Studio
- Vector DB Missing
- Ensure gemini-rag-small/ exists for cloud use
- Port Conflicts
- Change ports in api_server.py or app.py
- Import Errors
- Ensure src/ is in the Python path
- Verify required modules exist
- Debugging
- View logs in Railway dashboard
- Use /health endpoint

# 🤝 Contributing:
Fork the project
Create a feature branch
Commit changes
Push the branch
Create a Pull Request

# 🎉 Happy Chatting!
Feel free to star ⭐ the repository if you like it!
