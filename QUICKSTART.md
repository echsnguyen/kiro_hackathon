# ECH Scribe - Quick Start Guide

## 🎯 Choose Your Setup

### Option 1: Simple Demo (Recommended for Testing)
**No Docker, No Database, No Celery - Just Works!**

Perfect for: Quick demos, testing UI, presentations

```bash
# Terminal 1 - Backend
cd demo-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Terminal 2 - Frontend
cd demo
python -m http.server 8080

# Browser
# Open: http://localhost:8080
```

✅ **What you get:**
- Working web UI
- Synthetic data generation
- All features visible
- No setup complexity

---

### Option 2: Docker Setup (Full System)
**Complete backend with database, Redis, Celery**

Perfect for: Development, testing full features, production-like environment

#### Fix Celery Worker Issue:

The Celery worker needs the tasks module. I've created it, now run:

```bash
# Stop containers
docker-compose down

# Rebuild and start
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f celery_worker
```

#### If Celery Still Fails:

You can run without Celery for now:

```bash
# Start only essential services
docker-compose up -d postgres redis backend frontend

# Check what's running
docker-compose ps
```

The backend will work without Celery - async tasks just won't process in the background.

---

## 🚀 Using the Application

### Demo Version (Option 1):

1. **Open** http://localhost:8080
2. **Click through** the workflow steps at the top
3. **Try the Review step** - it's the most interesting:
   - Click on form fields to highlight transcript segments
   - Click on transcript segments to highlight them
   - Check validation boxes
   - Submit when all fields validated

### Docker Version (Option 2):

1. **Backend API**: http://localhost:8000
2. **API Docs**: http://localhost:8000/api/docs
3. **Frontend**: http://localhost:5173

---

## 🧪 Testing the Backend

### Demo Backend:
```bash
cd demo-backend
python test_api.py
```

### Docker Backend:
```bash
# Health check
curl http://localhost:8000/health

# Or open in browser
http://localhost:8000/api/docs
```

---

## 📊 What Each Setup Includes

### Demo (Simple):
- ✅ FastAPI backend with synthetic data
- ✅ HTML/CSS/JS frontend
- ✅ Realistic mock consultations
- ✅ All UI features working
- ❌ No real AI processing
- ❌ No database persistence
- ❌ No authentication

### Docker (Full):
- ✅ FastAPI backend
- ✅ React frontend
- ✅ PostgreSQL database
- ✅ Redis cache
- ✅ Celery worker (for async tasks)
- ✅ Complete architecture
- ⚠️ Requires AI API keys for full functionality
- ⚠️ More complex setup

---

## 🛑 Stopping the Application

### Demo:
Press `Ctrl+C` in each terminal

### Docker:
```bash
docker-compose down
```

---

## ⚠️ Troubleshooting

### Demo Issues:

**"Port already in use"**
```bash
# Backend - use different port
uvicorn main:app --port 8001

# Frontend - use different port
python -m http.server 8081
```

**"Module not found"**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate
pip install -r requirements.txt
```

### Docker Issues:

**"Celery worker not running"**
```bash
# Check logs
docker-compose logs celery_worker

# Restart just the worker
docker-compose restart celery_worker

# Or run without it
docker-compose up -d postgres redis backend frontend
```

**"Port conflicts"**
```bash
# Check what's using ports
netstat -ano | findstr :8000
netstat -ano | findstr :5432

# Stop all containers
docker-compose down

# Remove volumes if needed
docker-compose down -v
```

**"Database connection failed"**
```bash
# Wait for PostgreSQL to be ready
docker-compose logs postgres

# Restart backend after postgres is ready
docker-compose restart backend
```

---

## 💡 Recommendations

**For a quick demo or presentation:**
→ Use **Option 1 (Simple Demo)**

**For development or testing full features:**
→ Use **Option 2 (Docker)** but you can skip Celery for now

**For production:**
→ Follow the full setup in `SETUP.md` with proper configuration

---

## 🎓 Next Steps

1. **Try the demo** - Get familiar with the UI
2. **Generate synthetic data** - Use the API endpoints
3. **Explore the code** - See how it works
4. **Customize** - Modify the mock data or UI
5. **Build features** - Continue with the task list

---

## 📚 More Documentation

- **Demo Backend**: `demo-backend/README.md`
- **Demo Frontend**: `demo/README.md`
- **Full Setup**: `SETUP.md`
- **Project Structure**: `PROJECT_STRUCTURE.md`
- **Tasks**: `.kiro/specs/allied-health-assessment-automator/tasks.md`

---

Need help? Check the troubleshooting section above or review the detailed documentation files.
