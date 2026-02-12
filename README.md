# Emergency Routing System - Complete Stack

A modern web application for routing emergency patients to the most suitable hospital based on real-time requirements and resource availability.

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **MySQL** - Database for hospitals and emergency requests
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- MySQL database running

## 🚀 Setup Instructions

### 1. Backend Setup

#### Install Python Dependencies
```bash
cd EmergencyRoutingSystem
python -m venv emergency_env  # Create virtual environment
emergency_env\Scripts\activate  # Activate (Windows)
# or
source emergency_env/bin/activate  # (Mac/Linux)

pip install -r requirements.txt
```

#### Configure Database
Update `config.py` with your MySQL credentials:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'emergency_routing_db'
```

#### Run Backend
```bash
python app.py
# or
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

The API will be available at: `http://localhost:5000`
API Documentation: `http://localhost:5000/docs`

### 2. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Configure Environment
Create `.env` file:
```
REACT_APP_API_URL=http://localhost:5000/api
```

#### Run Frontend
```bash
npm start
```

The app will open at: `http://localhost:3000`

## 📊 API Endpoints

### Ambulance Routes
- `POST /api/ambulance/find-hospital` - Find nearest hospital
- `POST /api/ambulance/check-status` - Check request status
- `GET /api/ambulance/stats` - Get dashboard statistics

### Hospital Routes
- `GET /api/hospital/pending-requests` - Get pending requests
- `POST /api/hospital/accept-request` - Accept request
- `POST /api/hospital/reject-request` - Reject request

### Hospitals Route
- `GET /api/hospitals/` - Get all hospitals

## 🗄️ Database Schema

### Hospitals Table
```sql
CREATE TABLE hospitals (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  available_beds INT,
  available_icu INT,
  available_oxygen INT,
  available_ventilator INT
);
```

### Emergency Requests Table
```sql
CREATE TABLE emergency_requests (
  id INT PRIMARY KEY AUTO_INCREMENT,
  patient_type VARCHAR(50),
  emergency_type VARCHAR(50),
  need_bed BOOLEAN,
  need_icu BOOLEAN,
  need_oxygen BOOLEAN,
  need_ventilator BOOLEAN,
  hospital_id INT,
  status VARCHAR(50) DEFAULT 'Pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
);
```

## 🎯 Features

✅ **Ambulance Staff Panel**
- Submit emergency requests with patient details
- Select patient type and emergency type
- Choose required medical facilities
- Check request status in real-time

✅ **Hospital Admin Panel**
- View all pending emergency requests
- Accept/Reject requests with one click
- Auto-refresh every 10 seconds
- Real-time request management

✅ **Smart Hospital Matching**
- Finds nearest hospital with required facilities
- Uses Haversine formula for accurate distance calculation
- Filters by available resources (beds, ICU, oxygen, ventilators)

✅ **Modern UI/UX**
- Gradient-based beautiful design
- Responsive layout (mobile & desktop)
- Smooth animations
- Real-time statistics dashboard

## 🔄 Workflow

1. **Ambulance Staff** enters patient details and clicks "Find Nearest Hospital"
2. **System** calculates distance to all hospitals with required resources
3. **Hospital Admin** receives the request in their panel
4. **Hospital Admin** can Accept or Reject the request
5. **Ambulance Staff** sees the status update in real-time

## 📝 Project Structure

```
EmergencyRoutingSystem/
├── app.py                    # FastAPI main application
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── models/
│   ├── __init__.py
│   └── database.py          # Database operations
├── routes/
│   ├── ambulance.py         # Ambulance API routes
│   ├── hospital.py          # Hospital API routes
│   └── hospitals_list.py    # Hospitals list API
└── frontend/
    ├── package.json
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── public/
    │   └── index.html
    └── src/
        ├── index.js
        ├── index.css
        ├── App.js
        ├── api.js
        └── components/
            ├── AmbulancePanel.js
            ├── HospitalPanel.js
            └── StatsDashboard.js
```

## 🚨 Emergency Types Supported

- 🚗 Accident
- 💔 Attack
- 🫁 Respiratory

## 👤 Patient Types

- 🟢 Normal
- 🔴 Serious

## 📱 Medical Facilities

- 🛏️ Bed (Mandatory)
- 🏥 ICU
- 💨 Oxygen
- 🫁 Ventilator

## 🛠️ Development

To start both servers simultaneously in production:

### Terminal 1 - Backend
```bash
uvicorn app:app --host 0.0.0.0 --port 5000
```

### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

## 🐛 Troubleshooting

**CORS Error?**
- Ensure FastAPI CORS middleware is configured
- Check frontend API URL in `.env`

**Database Connection Failed?**
- Verify MySQL is running
- Check credentials in `config.py`
- Ensure database `emergency_routing_db` exists

**Frontend won't load?**
- Check if Node modules are installed: `npm install`
- Verify port 3000 is not in use

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Support

For issues or questions, please refer to the documentation or create an issue.
