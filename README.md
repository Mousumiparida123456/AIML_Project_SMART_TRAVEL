## Smart Travel Planner 

Smart Travel Planner is an AI-powered route optimization system that helps users find the best travel routes based on their preferences, persona, travel time, and constraints (like blocked cities).

It intelligently analyzes available routes and provides the most optimal plan along with a clear explanation.


## Features

1. Route Optimization
Choose from: Cheap, Fast, Comfortable, Balanced
2. Persona-Based Planning
Supports users like Student, Tourist, Business, etc.
3. Day/Night Travel Filtering
Customize routes based on travel time preference
4. Blocked Cities Handling
Exclude unwanted cities from routes
5.AI Recommendation
Explains why a route is selected
6. Interactive CLI Interface
Easy testing via terminal
7. Backend API Ready
Built with Flask for future web integration
8. Tech Stack

## Screenshots

<img width="1170" height="815" alt="Screenshot 2026-03-22 232157" src="https://github.com/user-attachments/assets/96c7e560-91c1-4bae-9755-ed00e562bc5a" />
<img width="1180" height="556" alt="Screenshot 2026-03-22 232249" src="https://github.com/user-attachments/assets/40f2510d-63d6-49c1-b19d-27a42c65cd57" />

## Layer	Technology

Backend	- Python, Flask
Data -	Pandas, CSV
Frontend - React, React-Leaflet
Deployment - Node.js / npm


## Project Structure

```
smart_travel/
│
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── search.py
│   ├── planner.py
│   ├── explainer.py
│   ├── constraints.py
│   ├── preferences.py
│   ├── advanced_features.py
│   ├── test.py
│   └── utils.py
│
├── data/
│   ├── routes.csv
│   └── blocked_cities.csv
│
├── package.json
├── .gitignore
└── README.md
```

 
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
