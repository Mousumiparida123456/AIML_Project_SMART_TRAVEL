# Smart Travel Planner

Smart Travel Planner is a small, learning-friendly travel route planner built around a simple CSV "routes database".
It's meant to be easy to run, easy to read, and good enough to demo common backend ideas (auth, APIs, shortest-path search).

At a glance:
- `backend/test.py`: an interactive CLI that filters and ranks routes by persona, preference, day/night, and blocked cities.
- `backend/app.py`: a Flask API with auth that returns a best route between two cities using Dijkstra's algorithm.

## Features

- Route preferences: Cheap, Fast, Comfortable, Balanced
- Persona-based planning (e.g., student, tourist, business)
- Day/night filtering (CLI demo)
- Blocked cities (CLI demo)
- Route explanation text ("AI-style" reasoning)
- API endpoints for auth + planning (`/register`, `/login`, `/plan`)

## Screenshots

<img width="1170" height="815" alt="Screenshot 2026-03-22 232157" src="https://github.com/user-attachments/assets/96c7e560-91c1-4bae-9755-ed00e562bc5a" />
<img width="1180" height="556" alt="Screenshot 2026-03-22 232249" src="https://github.com/user-attachments/assets/40f2510d-63d6-49c1-b19d-27a42c65cd57" />

## Layer	Technology

Backend	- Python, Flask
Data -	Pandas, CSV
Frontend - React, React-Leaflet
Deployment - Node.js / npm


## Project Structure

smart_travel/
  backend/
    app.py                 # Flask API (auth + /plan)
    auth.py                # In-memory users + JWT helpers
    search.py              # Dijkstra shortest-path (by cost/time/distance)
    planner.py             # Convert a path into a route summary
    explainer.py           # Text explanation for a chosen route
    constraints.py         # Constraint filters (building block for future)
    preferences.py         # Ranking helper (building block for future)
    advanced_features.py   # Switching penalty + random delay
    test.py                # Interactive CLI demo (recommended start)
    utils.py               # CSV -> graph loader
  data/
    routes.csv             # Route "database"
    blocked_cities.csv     # Block-list options for the CLI demo
  package.json             # (Placeholder) JS deps; no frontend app code here

 
 ## REPOSITORY LINK
https://github.com/Mousumiparida123456/AIML_Project_SMART_TRAVEL


## Setup & Installation
# Prerequisites
Python 3.x
Node.js (for frontend)


## Install Dependencies

# Backend dependencies
pip install flask pandas

# Frontend (optional for now)
npm install


## Run the Project (CLI Mode)
cd backend
python test.py


## How It Works (Flow)
1.Enter persona (e.g., Student)
2.Select travel time (Day/Night)
3.Choose blocked cities
4.Enter source city
5.Select destination
6.Choose preference (Cheap/Fast/etc.)


## Example Run
===== SMART TRAVEL PLAN INPUT =====
Persona: Student
Travel Time: Day
Blocked Cities: Hyderabad
Source: Chennai
Destination: Bangalore
Preference: Fast


## Output
===== BEST ROUTE =====
Path: Chennai → Bangalore
Cost: 300
Time: 6.0 hours
Distance: 350 km
Mode: Train
Switches: 0

AI Recommendation:
This route is selected as it takes the least time.


## Sample Scenario
# Input:
Persona: Student
Preference: Cheap
Blocked Cities: Delhi, Kolkata

# Output:
BEST ROUTE: Mumbai → Pune → Bangalore
Cost: ₹1200 | Time: 8.5h
Mode: Bus + Bus (1 switch)

AI: Cheapest option avoiding blocked cities.


## Future Enhancements
1. Web UI with map visualization
2. Live traffic & weather integration
3. Booking system integration
4. Advanced AI recommendations
5. Mobile app support


## Contributing
Contributions are welcome!
Feel free to fork the repo and submit a pull request.

## License
This project is open-source and available under the MIT License.
