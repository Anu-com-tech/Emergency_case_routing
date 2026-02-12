# 🚀 QUICK START GUIDE

## Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL Server running
- Terminal/Command Prompt

---

## ⚡ 5-Minute Setup (Windows)

### 1. Setup Database
```bash
# Open MySQL command line
mysql -u root -p

# Paste the contents of database_setup.sql
# Or run: mysql -u root -p < database_setup.sql
```

### 2. Backend Setup
```bash
# Double-click setup.bat
# OR run manually:

# Create virtual environment
python -m venv emergency_env

# Activate it
emergency_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python app.py
```

### 3. Frontend Setup (New Terminal)
```bash
cd frontend
npm install
npm start
```

### 4. Access Application
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- API Docs: http://localhost:5000/docs

---

## ⚡ 5-Minute Setup (Mac/Linux)

```bash
# 1. Setup Database
mysql -u root -p < database_setup.sql

# 2. Backend
bash setup.sh
source emergency_env/bin/activate
python app.py

# 3. Frontend (new terminal)
cd frontend
npm install
npm start

# 4. Open browser
open http://localhost:3000
```

---

## 🧪 Test the Application

### Test Ambulance Panel:
1. Go to http://localhost:3000
2. Select Patient Type: "🔴 Serious"
3. Select Emergency Type: "🚗 Accident"
4. Check ICU and Oxygen
5. Click "Find Nearest Hospital"
6. Copy Request ID

### Test Hospital Panel:
1. Scroll to right panel
2. See pending request
3. Click "✓ Accept" or "✗ Reject"
4. Request status updates automatically

### Test Status Check:
1. In Ambulance Panel
2. Paste Request ID in "Check Request Status"
3. Click "Check" button
4. See real-time status update

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 5000 already in use** | `netstat -ano \| findstr :5000` then kill process or use different port |
| **Port 3000 already in use** | Change in frontend or use `npm start -- --port 3001` |
| **MySQL Connection Error** | Verify MySQL is running and credentials in config.py match |
| **CORS Error** | Check if both servers are running |
| **API 404 Error** | Verify backend is running and URL is correct |

---

## 📝 Configuration

### Backend (.env or config.py):
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'emergency_routing_db'
```

### Frontend (.env):
```
REACT_APP_API_URL=http://localhost:5000/api
```

---

## 🎯 Next Steps

1. ✅ Get it running
2. ✅ Test all features
3. ✅ Add authentication (Optional)
4. ✅ Deploy to production

---

## 📞 Need Help?

- Read `README.md` for detailed docs
- Check `TRANSFORMATION_SUMMARY.md` for complete changelog
- Review FastAPI docs: http://localhost:5000/docs

🎉 **You're all set!**
