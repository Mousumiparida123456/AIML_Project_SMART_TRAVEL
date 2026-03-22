# Smart Travel Planner 🚀

## Overview
Smart Travel Planner is an AI-powered travel route optimization system that helps users find the best routes based on their preferences, persona, travel time, and constraints like blocked cities.

## Features
- ✅ Route optimization (Cheap, Fast, Comfortable, Balanced)
- ✅ Persona-based planning (Student, Tourist, Business, etc.)
- ✅ Day/Night travel filtering
- ✅ Blocked cities selection from predefined list
- ✅ Detailed route explanations with AI reasoning
- ✅ Interactive CLI test interface
- ✅ Flask backend API ready for web deployment

## Tech Stack
```
Frontend: React + React-Leaflet (Map integration)
Backend: Python Flask + Pandas
Data: CSV routes & blocked cities
Deployment: Node.js/npm for frontend
```

## Project Structure
```
smart_travel/
├── backend/          # Flask API modules
│   ├── app.py        # Main Flask app
│   ├── auth.py       # Authentication
│   ├── search.py     # Route search logic
│   ├── planner.py    # Route planning
│   ├── persona.py    # Persona handling
│   ├── preferences.py# Preference matching
│   └── test.py       # Interactive CLI tester ✅
├── data/             # Data files
│   ├── routes.csv    # Travel routes database
│   └── blocked_cities.csv # Blocked cities ✅
├── package.json      # Frontend dependencies
└── .gitignore        # Excludes node_modules, pycache
```

## Quick Setup & Test ✅

### Prerequisites
```bash
# Python dependencies
pip install flask pandas

# Frontend (if needed later)
npm install
```

### Test the CLI (Recommended first):
```bash
cd backend
python test.py
```
```
===== Flow =====
1. Enter persona: Student
2. Travel time: Day  
3. Blocked cities: 1,3 (Delhi, Kolkata)
4. Source: Mumbai
5. Destination: Bangalore
6. Preference: Cheap
```

**Sample Output:**
```
Blocked cities options:
1. Delhi
2. Mumbai  
3. Kolkata
...

BEST ROUTE: Mumbai → Pune → Bangalore
Cost: ₹1200 | Time: 8.5h | Bus + Bus (1 switch)
AI: Cheapest option avoiding blocked cities.
```

## Backend API Endpoints (Flask)
```bash
# Run server
cd backend
python app.py
```
```
GET /plan?source=Mumbai&dest=Bangalore&persona=Student&preference=cheap&blocked=Delhi,Kolkata
```

## Data Format

**routes.csv:**
```
source,destination,via,mode,cost,time,distance,switches,travel_time
Mumbai,Bangalore,"Pune;Hubli",Bus,1200,8.5,550,1,Day
```

**blocked_cities.csv:**
```
city
Delhi
Mumbai
...
```

## Run Full Stack (Future)
```bash
# Backend
cd backend && python app.py

# Frontend  
npm start
```

## GitHub Repo
https://github.com/Mousumiparida123456/AIML_Project_SMART_TRAVEL

## Future Scope
- ML dynamic pricing/traffic prediction
- React Native mobile app
- Real-time Google Maps
- AWS cloud deployment
- OAuth2 authentication
- Analytics dashboard
- Multi-country routes

## License
**MIT License** - Permissive open source license allowing:
- Free use, copy, modify, distribute (commercial/private OK)
- No warranty
- Must keep copyright/license notice
- Used by React, Node.js, Rails
