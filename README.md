# LabMate AI - Backend API 🧪

**Your AI-Powered STEM Learning Assistant**

LabMate AI helps university students with lab reports, research papers, and finding quality educational resources.

---

## 🚀 Features

### 1. **Lab Report Generator**
- Generate complete, formatted lab reports from experimental data
- Includes: Introduction, Theory, Materials, Procedure, Results, Discussion, Conclusion
- Export-ready format

### 2. **Research Paper Finder & Summarizer**
- Search arXiv and Semantic Scholar for relevant papers
- Get brief or detailed summaries
- Extract key concepts
- Find related papers

### 3. **Educational Video Finder**
- Find curated YouTube videos for any topic
- Ranked by quality and relevance
- Filter by difficulty level (beginner/intermediate/advanced)
- Create learning playlists

### 4. **AI Study Assistant**
- Chat with AI about STEM concepts
- Get detailed concept explanations
- Solve formulas step-by-step
- Check your work and get feedback

---

## 📋 Prerequisites

- **Python 3.8+** (You have 3.14 ✅)
- **pip** (Python package manager)
- **Git** (for version control)

---

## ⚙️ Setup Instructions

### Step 1: Clone/Navigate to Project
```bash
cd labmate-backend
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your API keys
# You can use notepad or any text editor
notepad .env
```

**Get Your FREE API Keys:**

1. **Groq API** (Required for AI features)
   - Go to: https://console.groq.com
   - Sign up (free)
   - Create an API key
   - Paste it in `.env`: `GROQ_API_KEY=your_key_here`

2. **YouTube API** (Optional - for video search)
   - Go to: https://console.cloud.google.com
   - Create a project
   - Enable "YouTube Data API v3"
   - Create credentials (API key)
   - Paste it in `.env`: `YOUTUBE_API_KEY=your_key_here`

### Step 5: Run the Server
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 6: Test It!
Open a new terminal and test:
```bash
curl http://127.0.0.1:5000/health
```

You should get:
```json
{
  "status": "healthy",
  "timestamp": "2024-02-16T...",
  "version": "1.0.0"
}
```

🎉 **Your backend is running!**

---

## 🔌 API Endpoints

### Health Check
```
GET /health
```

### Lab Report Generator

#### Generate Complete Report
```
POST /api/generate-report
Content-Type: application/json

{
  "title": "Titration Experiment",
  "course_code": "CH 273",
  "objective": "To determine the concentration of NaOH solution",
  "materials": ["Burette", "Pipette", "NaOH solution", "HCl solution"],
  "procedure": "1. Fill burette with NaOH...",
  "observations": "Initial reading: 0.0ml, Final reading: 25.5ml",
  "data": [
    {"trial": 1, "volume": 25.5},
    {"trial": 2, "volume": 25.3}
  ]
}
```

#### Format Raw Notes
```
POST /api/format-report
Content-Type: application/json

{
  "raw_notes": "We heated the solution and observed color change...",
  "report_type": "chemistry"
}
```

### Research Papers

#### Search Papers
```
POST /api/search-papers
Content-Type: application/json

{
  "query": "heat transfer in chemical processes",
  "max_results": 10
}
```

#### Summarize Paper
```
POST /api/summarize-paper
Content-Type: application/json

{
  "paper_url": "https://arxiv.org/abs/2301.12345",
  "summary_type": "brief"
}
```

### Video Resources

#### Find Videos
```
POST /api/find-videos
Content-Type: application/json

{
  "topic": "organic chemistry reactions",
  "course_code": "CH 257",
  "max_results": 10,
  "difficulty": "intermediate"
}
```

#### Create Learning Playlist
```
POST /api/curate-playlist
Content-Type: application/json

{
  "course_code": "CH 275",
  "topics": ["titration", "pH calculations", "buffer solutions"]
}
```

### AI Assistant

#### Chat
```
POST /api/chat
Content-Type: application/json

{
  "message": "Explain Le Chatelier's principle",
  "context": "CH 263 - Chemical Thermodynamics",
  "conversation_history": []
}
```

#### Explain Concept
```
POST /api/explain-concept
Content-Type: application/json

{
  "concept": "enthalpy",
  "level": "undergraduate",
  "include_examples": true
}
```

#### Solve Formula
```
POST /api/solve-formula
Content-Type: application/json

{
  "formula": "PV = nRT",
  "known_values": {
    "P": 101.325,
    "V": 22.4,
    "T": 273.15
  },
  "solve_for": "n"
}
```

---

## 📁 Project Structure

```
labmate-backend/
├── app.py                 # Main Flask application
├── ai_service.py         # AI/LLM integration (Groq API)
├── report_generator.py   # Lab report generation
├── video_service.py      # YouTube video search
├── research_service.py   # Research paper search (arXiv)
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

---

## 🧪 Testing the API

### Using cURL (Command Line)

**Test Health:**
```bash
curl http://127.0.0.1:5000/health
```

**Generate Lab Report:**
```bash
curl -X POST http://127.0.0.1:5000/api/generate-report \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Test Experiment\",\"course_code\":\"CH 273\",\"objective\":\"Test objective\",\"procedure\":\"Step 1...\",\"observations\":\"We observed...\"}"
```

### Using Python (requests library)

```python
import requests

# Test health
response = requests.get('http://127.0.0.1:5000/health')
print(response.json())

# Generate report
data = {
    "title": "Titration Experiment",
    "course_code": "CH 273",
    "objective": "Determine NaOH concentration",
    "procedure": "Fill burette...",
    "observations": "Color changed from clear to pink"
}

response = requests.post(
    'http://127.0.0.1:5000/api/generate-report',
    json=data
)
print(response.json())
```

### Using Postman
1. Download Postman: https://www.postman.com/downloads/
2. Create new request
3. Set method to POST
4. URL: `http://127.0.0.1:5000/api/generate-report`
5. Headers: `Content-Type: application/json`
6. Body: Select "raw" and paste JSON data

---

## 🚢 Deployment Options

### Option 1: Render (Recommended - FREE)
1. Create account at https://render.com
2. Connect your GitHub repo
3. Create new "Web Service"
4. Set environment variables in Render dashboard
5. Deploy!

### Option 2: Railway (Easy, FREE tier)
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repo
4. Add environment variables
5. Deploy!

### Option 3: Heroku (Popular)
1. Create Heroku account
2. Install Heroku CLI
3. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
4. Deploy:
   ```bash
   heroku create labmate-api
   git push heroku main
   ```

---

## 🔧 Development Tips

### Running in Debug Mode
```bash
# Automatic reload when you edit code
export FLASK_ENV=development  # macOS/Linux
set FLASK_ENV=development     # Windows
python app.py
```

### Checking Logs
```bash
# The console will show all requests and errors
# Look for error messages if something doesn't work
```

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`
**Fix**: Make sure virtual environment is activated and run `pip install -r requirements.txt`

**Issue**: `KeyError: 'GROQ_API_KEY'`
**Fix**: Check that `.env` file exists and contains your API key

**Issue**: Port 5000 already in use
**Fix**: Change port in `.env`: `PORT=5001`

---

## 📊 API Response Examples

### Successful Response
```json
{
  "success": true,
  "report": {
    "title": "Titration Experiment",
    "course_code": "CH 273",
    "sections": {
      "introduction": "...",
      "theory": "...",
      "procedure": "...",
      "results": "...",
      "discussion": "...",
      "conclusion": "..."
    }
  },
  "generated_at": "2024-02-16T10:30:00"
}
```

### Error Response
```json
{
  "error": "Missing required field: title",
  "status": 400
}
```

---

## 🎯 Next Steps

1. **Test all endpoints** using cURL or Postman
2. **Build the mobile app frontend** with FlutterFlow
3. **Deploy to Render/Railway** for production
4. **Connect mobile app** to deployed API
5. **Get feedback** from classmates
6. **Iterate and improve!**

---

## 💡 Cost Breakdown (Monthly)

- **Groq API**: FREE tier includes generous limits
- **YouTube API**: FREE (10,000 requests/day)
- **arXiv API**: FREE (no limits)
- **Hosting (Render)**: FREE tier available
- **Domain** (optional): $10-15/year

**Total: $0-5/month for MVP!** 🎉

---

## 🤝 Support

Having issues? Check:
1. Is virtual environment activated?
2. Are all dependencies installed? (`pip install -r requirements.txt`)
3. Is `.env` file configured with API keys?
4. Is the server running? (`python app.py`)
5. Are you using the correct port (5000)?

---

## 📝 License

MIT License - Free to use and modify!

---

**Built with ❤️ for STEM Students**

Good luck with your labs! 🧪🔬
