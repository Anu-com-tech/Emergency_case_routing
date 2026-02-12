#!/bin/bash
# Emergency Routing System - Startup Script

echo "🚑 Emergency Routing System Startup"
echo "=================================="

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${RED}Python is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "emergency_env" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python -m venv emergency_env
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source emergency_env/bin/activate

# Install/upgrade dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Install frontend dependencies
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "To start the application, run these commands in separate terminals:"
echo ""
echo -e "${YELLOW}Terminal 1 (Backend):${NC}"
echo "  source emergency_env/bin/activate  # For Mac/Linux"
echo "  # or"
echo "  emergency_env\\Scripts\\activate  # For Windows"
echo "  python app.py"
echo ""
echo -e "${YELLOW}Terminal 2 (Frontend):${NC}"
echo "  cd frontend"
echo "  npm start"
echo ""
echo -e "${GREEN}Frontend will open at: http://localhost:3000${NC}"
echo -e "${GREEN}Backend API at: http://localhost:5000${NC}"
echo -e "${GREEN}API Docs at: http://localhost:5000/docs${NC}"
