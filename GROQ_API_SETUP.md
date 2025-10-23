# 🤖 Groq API Setup Guide

## Why Groq?

**Groq** provides **FREE**, **FAST**, and **POWERFUL** AI inference with:
- ✅ **Free API** with generous limits
- ✅ **Lightning fast** responses (10x faster than OpenAI)
- ✅ **No credit card** required
- ✅ **Llama 3.1 70B** model (state-of-the-art)
- ✅ **Easy integration** with OpenAI-compatible API

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create Groq Account

1. Go to [https://console.groq.com](https://console.groq.com)
2. Click **"Sign Up"** or **"Get Started"**
3. Sign up with:
   - Google account (recommended)
   - GitHub account
   - Email + password

### Step 2: Get API Key

1. After login, go to [https://console.groq.com/keys](https://console.groq.com/keys)
2. Click **"Create API Key"**
3. Give it a name: `InterviewAce`
4. Click **"Submit"**
5. **Copy the API key immediately** (you won't see it again!)

Example key format:
```
gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 3: Add to .env File

Open your `.env` file and add:

```env
# AI Configuration (Groq API)
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### Step 4: Install Dependencies

```bash
pip install groq requests
```

Or update all dependencies:
```bash
pip install -r requirements.txt
```

### Step 5: Test the Setup

Run your application:
```bash
python app.py
```

Start an interview and check if AI questions are generated!

---

## 📊 Groq Free Tier Limits

| Feature | Free Tier |
|---------|-----------|
| **Requests per minute** | 30 |
| **Requests per day** | 14,400 |
| **Tokens per minute** | 6,000 |
| **Cost** | $0 (FREE) |

**Perfect for:**
- Development and testing
- Small to medium applications
- Personal projects
- MVP launches

---

## 🎯 What Groq Does in InterviewAce

### 1. **Question Generation**
```
Input: Role (Software Engineer) + Level (Intermediate)
Output: 10 tailored interview questions (3 MCQ + 7 written)
```

### 2. **Answer Evaluation**
```
Input: Question + User's answer
Output: Score (0-20) + Detailed feedback
```

### 3. **Comprehensive Report**
```
Input: All answers + questions
Output: Performance summary, strengths, improvements, recommendations
```

---

## 🔧 Alternative AI Providers

If you prefer other providers, you can easily switch:

### Option 1: OpenAI (Paid)
```env
OPENAI_API_KEY=sk-your-key
```

Update `ai_service.py`:
```python
API_URL = 'https://api.openai.com/v1/chat/completions'
MODEL = 'gpt-3.5-turbo'
```

### Option 2: Hugging Face (Free)
```env
HUGGINGFACE_API_KEY=hf_your-key
```

Update `ai_service.py`:
```python
API_URL = 'https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf'
```

### Option 3: Anthropic Claude (Paid)
```env
ANTHROPIC_API_KEY=sk-ant-your-key
```

---

## 🧪 Testing Groq Integration

### Test 1: Question Generation

```bash
curl -X GET "http://localhost:5000/api/questions?role=Software%20Engineer&difficulty=Intermediate&use_ai=true"
```

Expected response:
```json
{
  "success": true,
  "questions": [...],
  "source": "ai"
}
```

### Test 2: Answer Evaluation

Start an interview, answer questions, and submit. Check console logs for:
```
AI evaluation: {"score": 18, "feedback": "Excellent answer..."}
```

---

## 🐛 Troubleshooting

### Issue 1: "Invalid API Key"

**Error:**
```
401 Unauthorized: Invalid API key
```

**Solution:**
1. Check if API key is correct in `.env`
2. Ensure no extra spaces around the key
3. Regenerate API key from Groq console

### Issue 2: "Rate Limit Exceeded"

**Error:**
```
429 Too Many Requests
```

**Solution:**
1. Wait 1 minute (free tier: 30 requests/min)
2. Reduce concurrent interviews
3. Implement caching for questions

### Issue 3: "Connection Timeout"

**Error:**
```
Timeout after 30 seconds
```

**Solution:**
1. Check internet connection
2. Increase timeout in `ai_service.py`:
   ```python
   timeout=60  # Increase from 30 to 60
   ```

### Issue 4: "Module Not Found: groq"

**Error:**
```
ModuleNotFoundError: No module named 'groq'
```

**Solution:**
```bash
pip install groq requests
```

---

## 📈 Performance Optimization

### 1. Cache Questions
```python
# Cache generated questions for 1 hour
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_questions(role, level):
    return AIService.generate_interview_questions(role, level)
```

### 2. Async Processing
```python
# Evaluate answers in parallel
import asyncio

async def evaluate_all_answers(answers, questions):
    tasks = [evaluate_answer(q, a) for q, a in zip(questions, answers)]
    return await asyncio.gather(*tasks)
```

### 3. Fallback System
The system automatically falls back to static questions if:
- API key is missing
- Rate limit exceeded
- Network error
- API timeout

---

## 🔐 Security Best Practices

### 1. Never Commit API Keys
```bash
# Add to .gitignore
.env
*.env
```

### 2. Use Environment Variables
```python
# ✅ Good
API_KEY = os.getenv('GROQ_API_KEY')

# ❌ Bad
API_KEY = 'gsk_hardcoded_key'
```

### 3. Rotate Keys Regularly
- Regenerate API keys every 3 months
- Use different keys for dev/prod

### 4. Monitor Usage
- Check Groq dashboard regularly
- Set up usage alerts
- Track API costs (if upgraded to paid)

---

## 📚 Additional Resources

- **Groq Documentation**: https://console.groq.com/docs
- **Groq Playground**: https://console.groq.com/playground
- **API Reference**: https://console.groq.com/docs/api-reference
- **Community**: https://discord.gg/groq

---

## ✅ Setup Checklist

Before running the application:

- [ ] Groq account created
- [ ] API key generated
- [ ] API key added to `.env` file
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Application starts without errors
- [ ] Test interview generates AI questions
- [ ] Answer evaluation works
- [ ] Comprehensive report generated

---

## 🎉 You're All Set!

Your InterviewAce application now has:
- ✅ AI-powered question generation
- ✅ Intelligent answer evaluation
- ✅ Comprehensive performance reports
- ✅ Free and fast AI inference

**Start interviewing with AI! 🚀**
