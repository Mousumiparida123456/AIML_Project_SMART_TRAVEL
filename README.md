# Smart Travel Planner

Smart Travel Planner is a small, learning-friendly travel route planner built around a simple CSV "routes database".
It's meant to be easy to run, easy to read, and good enough to demo common backend ideas (auth, APIs, shortest-path search).

At a glance:

- `backend/test.py`: an interactive CLI that filters and ranks routes by persona, preference, day/night, and blocked cities.
- `backend/app.py`: a Flask API with auth that returns a best route between two cities using Dijkstra's algorithm.

## What's in this repo (and what isn't)

Included:

- Interactive CLI planner (persona + preference + day/night + blocked cities)
- Flask API with `/register`, `/login`, and `/plan`
- Route explanation text (simple "AI-style" reasoning)
- Sample data in `data/routes.csv` and `data/blocked_cities.csv`

Not included (yet):

- A working React frontend UI (only a minimal `package.json` exists; there is no `src/` app in this repository)
- Persistent database (users are stored in-memory and reset when the server restarts)

## Tech Stack

- Backend: Python + Flask
- CLI demo: Python + Pandas
- Auth: JWT (PyJWT)
- Data: CSV files in `data/`

## Project Structure

```
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
```

## Quick Start (CLI demo)

### 1) Prerequisites

- Python 3.8+

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2) Run the CLI

```bash
cd backend
python test.py
```

The CLI will walk you through:

- Persona (example: `Student`, `Tourist`)
- Travel time (`Day` or `Night`)
- Blocked cities (pick from the menu; optional)
- Source and destination (chosen from available cities in `data/routes.csv`)
- Preference (`Cheap`, `Fast`, `Comfortable`, `Balanced`)

Note: the CLI demo ranks the route options available in `data/routes.csv` (including any intermediate stops listed in the `via` column). It does not run Dijkstra across the whole graph.

## Run the Flask API

Start the server from the `backend/` directory (important: the app loads `../data/routes.csv` using a relative path):

```bash
cd backend
python app.py
```

The API runs at `http://127.0.0.1:5000` by default.

### Auth endpoints (PowerShell)

Register:

```powershell
$base = "http://127.0.0.1:5000"
Invoke-RestMethod "$base/register" -Method Post -ContentType "application/json" -Body (@{ username="demo"; password="demo" } | ConvertTo-Json)
```

Login (returns a JWT token):

```powershell
$token = (Invoke-RestMethod "$base/login" -Method Post -ContentType "application/json" -Body (@{ username="demo"; password="demo" } | ConvertTo-Json)).token
$token
```

### Plan endpoint

`/plan` currently:

- Requires an `Authorization` header (supports both raw token and `Bearer <token>`)
- Accepts JSON `source` + `destination`, and optionally:
  - `preference`: `cheap`, `fast`, `distance`/`short`, `comfortable`, `balanced`
  - `persona`: `student`, `business`, `tourist`, `eco` (used as a fallback to set preference)
  - `travel_time`: `day` or `night`
  - `blocked_cities`: list (or comma-separated string)
  - `constraints`: `max_cost`, `max_time`, `max_transfers`, `preferred_mode`
  - `apply_switch_penalty` (bool) and `switching_penalty` (int, default `50`)
  - `simulate_delay` (bool) to add a random delay (`0`-`2` hours)

Example:

```powershell
Invoke-RestMethod "$base/plan" -Method Post -ContentType "application/json" -Headers @{ Authorization = $token } -Body (@{ source="Delhi"; destination="Goa" } | ConvertTo-Json)
```

Response shape (simplified):

```json
{
  "user": "demo",
  "route": {
    "path": ["Delhi", "Mumbai", "Goa"],
    "total_time": 28,
    "total_cost": 1600,
    "total_distance": 2000,
    "modes": ["train", "bus"],
    "transfers": 2,
    "mode_switches": 1,
    "switch_penalty": 50,
    "delay_added": 1
  }
}
```

## Data Files

### `data/routes.csv`

Columns:

- `source`, `destination`: city names (strings)
- `via`: optional intermediate stops separated by `;` (used by the CLI demo)
- `cost`, `time`, `distance`: numeric values used for ranking / shortest-path
- `mode`: example `train`, `bus`
- `switches`: number of switches (used by the CLI demo)
- `travel_time`: `day` or `night` (used by the CLI demo)

Important behavior:

- The Flask API loads routes into a graph and automatically adds a reverse edge for every row (so routes behave like "two-way" connections).
- For the Flask API graph, only `source`, `destination`, `mode`, `time`, `cost`, and `distance` are used. The CLI demo also uses `via`, `switches`, and `travel_time`.

### `data/blocked_cities.csv`

- One column: `city`
- Used only by the CLI demo to exclude routes that pass through blocked cities.

## Troubleshooting

- If `backend/app.py` fails to find `../data/routes.csv`, make sure you started the server from inside `backend/` (`cd backend` first).
- If `/plan` returns `403 Unauthorized`, confirm you sent the token in the `Authorization` header exactly as returned by `/login`.

## Future Scope / Ideas

- Apply persona + constraints in the API (blocked cities, day/night, max cost/time, preferred mode)
- Return multiple candidate routes (top N)
- Persistent storage for users (replace in-memory dict)
- Build a real frontend UI (map visualization, search form)

## Repository link

If you are viewing this project as a fork or copy, the original repo link (if applicable) is:
`https://github.com/Mousumiparida123456/AIML_Project_SMART_TRAVEL`

## License

No `LICENSE` file is included in this repository yet. Add one (for example MIT) if you plan to publish or reuse this code outside a class/project setting.
