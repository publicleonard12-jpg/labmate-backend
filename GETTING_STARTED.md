# 🚀 LabMate AI - Getting Started Guide

## Welcome! Let's Get Your Backend Running in 10 Minutes

This guide will walk you through setting up the LabMate AI backend step-by-step.

---

## 📍 Step 1: Verify Your Setup

Open Command Prompt (CMD) and check:

```bash
python --version
```
✅ You should see: `Python 3.14.x` (or similar)

```bash
git --version
```
✅ You should see git version info

---

## 📦 Step 2: Get the Code

You already have the code! Navigate to it:

```bash
cd path\to\labmate-backend
```

Check files are there:
```bash
dir
```

You should see:
- `app.py`
- `ai_service.py`
- `report_generator.py`
- `video_service.py`
- `research_service.py`
- `requirements.txt`
- `start.bat`
- And more...

---

## ⚡ Step 3: Quick Start (Easiest Way)

Just double-click `start.bat` or run:

```bash
start.bat
```

This will:
1. Create a virtual environment
2. Install all dependencies
3. Create .env file (if needed)
4. Start the server

**That's it!** 🎉

---

## 🔧 Step 4: Manual Setup (If You Prefer)

### 4.1 Create Virtual Environment

```bash
python -m venv venv
```

### 4.2 Activate Virtual Environment

```bash
venv\Scripts\activate
```

Your prompt should now show `(venv)` at the start.

### 4.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4.4 Set Up Environment Variables

```bash
copy .env.example .env
notepad .env
```

Add your API keys (see Step 5 below).

### 4.5 Start the Server

```bash
python app.py
```

---

## 🔑 Step 5: Get Your FREE API Keys

### 5.1 Groq API Key (REQUIRED for AI features)

**Why Groq?**
- Super fast responses
- Very affordable (10-20x cheaper than OpenAI)
- Generous free tier
- No credit card required for signup!

**How to get it:**

1. Go to: https://console.groq.com
2. Click "Sign Up" (use your email or Google account)
3. Verify your email
4. Click "API Keys" in the left sidebar
5. Click "Create API Key"
6. Give it a name like "LabMate-Dev"
7. Copy the key (starts with `gsk_...`)
8. Open `.env` and paste:
   ```
   GROQ_API_KEY=gsk_your_key_here
   ```

**Models Available:**
- `llama-3.3-70b-versatile` (Default - Fast & Smart)
- `mixtral-8x7b-32768` (Longer context)
- `llama-3.1-8b-instant` (Ultra fast)

### 5.2 YouTube API Key (OPTIONAL for video search)

**If you skip this:** Video search will return mock data (still works for testing)

**How to get it:**

1. Go to: https://console.cloud.google.com
2. Create a Google Cloud account (free)
3. Create a new project: "LabMate"
4. Enable "YouTube Data API v3":
   - Search for it in the search bar
   - Click "Enable"
5. Create credentials:
   - Click "Credentials" in left sidebar
   - "Create Credentials" → "API Key"
   - Copy the key
6. Open `.env` and paste:
   ```
   YOUTUBE_API_KEY=your_key_here
   ```

**Free Tier Limits:**
- 10,000 requests per day
- More than enough for testing and initial users!

---

## ✅ Step 6: Test Your Setup

### 6.1 Is the Server Running?

You should see something like:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 6.2 Test Health Check

Open a **new** Command Prompt and run:

```bash
curl http://127.0.0.1:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-02-16T...",
  "version": "1.0.0"
}
```

✅ If you see this, your backend is working!

### 6.3 Run Full Test Suite

```bash
python test_api.py
```

This will test ALL endpoints and show you what's working.

---

## 📱 Step 7: Test with Real Data

### Test Lab Report Generation

Create a file `test_report.py`:

```python
import requests
import json

data = {
    "title": "My First Lab Report",
    "course_code": "CH 273",
    "objective": "Test the LabMate AI system",
    "materials": ["Flask", "Beaker", "Computer"],
    "procedure": "1. Open LabMate\n2. Generate report\n3. Be amazed",
    "observations": "The system works perfectly!"
}

response = requests.post(
    'http://127.0.0.1:5000/api/generate-report',
    json=data
)

result = response.json()
print(json.dumps(result, indent=2))
```

Run it:
```bash
python test_report.py
```

You should get a complete lab report! 🎉

---

## 🐛 Troubleshooting

### Problem: "Python not found"
**Solution:** Make sure Python is installed and added to PATH

### Problem: "pip not found"
**Solution:** Use `python -m pip` instead of `pip`

### Problem: "Module not found: flask"
**Solution:** 
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: "Port 5000 already in use"
**Solution:** Edit `.env` and change:
```
PORT=5001
```

### Problem: "API responses say [MOCK RESPONSE]"
**Solution:** You haven't set your GROQ_API_KEY in `.env`

### Problem: "Connection refused"
**Solution:** Make sure the server is running in another terminal

### Problem: "Video search returns mock data"
**Solution:** Add your YOUTUBE_API_KEY to `.env` (or keep using mock data for testing)

---

## 📊 Understanding the Response

### Successful Response:
```json
{
  "success": true,
  "report": { ... },
  "generated_at": "2024-02-16T10:30:00"
}
```

### Error Response:
```json
{
  "error": "Missing required field: title",
  "status": 400
}
```

---

## 🎯 Next Steps After Backend is Working

1. **Test with Your Real Lab Data**
   - Use data from your actual experiments
   - See how accurate the reports are

2. **Deploy to Production**
   - Follow deployment guide in README.md
   - Render.com has a free tier!

3. **Build Mobile Frontend**
   - Use FlutterFlow
   - Connect to your deployed backend
   - Or connect to localhost for testing

4. **Get Feedback**
   - Share with 2-3 classmates
   - Collect their thoughts
   - Iterate!

---

## 💰 Cost Tracking

### Current Costs (per month):
- **Groq API**: $0 (free tier)
- **YouTube API**: $0 (10k requests/day free)
- **arXiv API**: $0 (always free)
- **Hosting (local)**: $0

### When You Deploy:
- **Render.com**: $0 (free tier) or $7/month (paid)
- **Railway**: $0 (free tier) or $5/month (paid)
- **Domain**: ~$1/month (optional)

**Total: $0-8/month** 🎉

---

## 📞 Need Help?

### Common Questions:

**Q: Can I run this without API keys?**
A: Yes! It will return mock data for testing.

**Q: How much does Groq cost after free tier?**
A: Very cheap - about $0.10 per 1M tokens (much cheaper than OpenAI)

**Q: Can multiple people use this at once?**
A: Yes! Once deployed, unlimited users can access it.

**Q: Will this work on my school timetable?**
A: Absolutely! Backend runs 24/7 once deployed. You can use it anytime.

**Q: What if I get stuck?**
A: Check the error messages, look at the test output, and review the README.md

---

## 🎓 Your Development Schedule

Based on your timetable:

**Weekends** (Big work sessions):
- Saturday: 3-4 hours → Backend testing & refinement
- Sunday: 3-4 hours → Start FlutterFlow frontend

**Weekdays** (Quick sessions):
- **Monday mornings** (before 11am class): 1-2 hours
- **Wednesday evenings** (after 5:30pm): 1 hour  
- **Late nights** (when you have energy): 30min-1hr

**Total weekly time: 10-15 hours** (very doable!)

---

## ✅ Success Checklist

Before moving to frontend, make sure:

- [ ] Backend starts without errors
- [ ] Health check returns "healthy"
- [ ] Lab report generation works
- [ ] Video search returns results (mock is OK)
- [ ] Research paper search works
- [ ] AI chat responds
- [ ] All tests pass (test_api.py)
- [ ] You understand how to use each endpoint
- [ ] .env file has your API keys
- [ ] You've tested with real lab data

---

**You're ready to build something amazing! 🚀**

When you're done testing the backend, switch back to **Leo** mode and we'll work on:
1. Deployment strategy
2. Mobile frontend with FlutterFlow
3. User testing plan
4. NegotiateAI and LocalGenius prototypes

Good luck! 🧪📱
