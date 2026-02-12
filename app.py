from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Config
from models.database import Database
from routes.ambulance import ambulance_router, set_db as set_ambulance_db
from routes.hospital import hospital_router, set_db as set_hospital_db
from routes.hospitals_list import hospitals_router, set_db as set_hospitals_db


app = FastAPI(
    title="Emergency Routing System",
    version="1.0.0"
)

# -------------------------
# Enable CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# STARTUP EVENT (KEY FIX 🔑)
# -------------------------
@app.on_event("startup")
def startup_event():
    print("Initializing database...")
    config = Config()
    db = Database(config)

    print("Connecting to database...")
    if not db.connect():
        raise RuntimeError("Database connection failed")

    print("[OK] Database connection successful")

    # store db
    app.state.db = db

    # pass db to routes
    set_ambulance_db(db)
    set_hospital_db(db)
    set_hospitals_db(db)


# -------------------------
# SHUTDOWN EVENT
# -------------------------
@app.on_event("shutdown")
def shutdown_event():
    db = app.state.db
    if db:
        print("Closing database connection...")
        db.disconnect()
        print("Database disconnected")


# -------------------------
# Health check
# -------------------------
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Emergency Routing System API is running"
    }


# -------------------------
# Routers
# -------------------------
app.include_router(ambulance_router, prefix="/api/ambulance", tags=["Ambulance"])
app.include_router(hospital_router, prefix="/api/hospital", tags=["Hospital"])
app.include_router(hospitals_router, prefix="/api/hospitals", tags=["Hospitals"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
