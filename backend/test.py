import pandas as pd
import os

# ---------------------------
# Step 1: Load CSV file
# ---------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
routes_file = os.path.join(current_dir, "..", "data", "routes.csv")

try:
    routes_df = pd.read_csv(routes_file)
except FileNotFoundError:
    print(f"Error: Could not find routes.csv at {routes_file}")
    exit()

# Convert 'via' column to list
def parse_via(via_str):
    if pd.isna(via_str) or via_str.strip() == "":
        return []
    return [city.strip() for city in via_str.split(";")]

routes = routes_df.to_dict(orient='records')
for r in routes:
    r['via'] = parse_via(r.get('via', ''))
    r['switches'] = int(r.get('switches', 0))
    r['cost'] = float(r.get('cost', 0))
    r['time'] = float(r.get('time', 0))
    r['distance'] = float(r.get('distance', 0))

# ---------------------------
# Step 2: AI-style explanation
# ---------------------------
def explain_plan(plan, preference):
    explanation = ""
    if preference.lower() == "cheap":
        explanation = f"This route is chosen because it has the lowest cost ({plan['total_cost']})."
    elif preference.lower() == "fast":
        explanation = f"This route is selected as it takes the least time ({plan['total_time']} hours)."
    elif preference.lower() == "comfortable":
        explanation = f"This route is more comfortable with only {plan['mode_switches']} transport switches."
    elif preference.lower() == "balanced":
        explanation = f"This route provides a balance between cost ({plan['total_cost']}) and time ({plan['total_time']} hours)."
    else:
        explanation = "This route is optimal based on selected preference."

    explanation += f" It includes {len(plan['path']) - 1} stops and uses {', '.join(plan['modes'])} transport."
    return explanation

# ---------------------------
# Step 3: Ask user details
# ---------------------------
print("===== SMART TRAVEL PLAN INPUT =====")
persona = input("Enter your persona (e.g., Student, Tourist): ").strip()
travel_time = input("Enter travel time (Day/Night): ").strip()
# Load blocked cities CSV
blocked_file = os.path.join(current_dir, "..", "data", "blocked_cities.csv")
try:
    blocked_df = pd.read_csv(blocked_file)
    blocked_cities_list = blocked_df['city'].tolist()
except FileNotFoundError:
    print(f"Error: Could not find blocked_cities.csv at {blocked_file}")
    blocked_cities_list = []

print("\nBlocked cities options:")
for idx, city in enumerate(blocked_cities_list, 1):
    print(f"{idx}. {city}")

if blocked_cities_list:
    selection_input = input("Enter blocked city numbers separated by commas (e.g., 1,3) or leave blank for none: ").strip()
    if selection_input:
        try:
            indices = [int(i.strip()) - 1 for i in selection_input.split(',')]
            blocked_cities = [blocked_cities_list[i] for i in indices if 0 <= i < len(blocked_cities_list)]
        except ValueError:
            print("Invalid input. No blocked cities selected.")
            blocked_cities = []
    else:
        blocked_cities = []
else:
    blocked_cities = []

# ---------------------------
# Step 4: Show available sources
# ---------------------------
all_sources = sorted(set(r['source'] for r in routes))
print(f"\nAvailable source cities: {', '.join(all_sources)}")
while True:
    source = input("Enter source city from the above options: ").strip()
    if source in all_sources:
        break
    print("Invalid source. Please select from the available options.")

# ---------------------------
# Step 5: Show available destinations based on source
# ---------------------------
available_destinations = sorted(set(r['destination'] for r in routes if r['source'] == source))
print(f"Available destinations from {source}: {', '.join(available_destinations)}")
while True:
    destination = input("Enter destination city from the above options: ").strip()
    if destination in available_destinations:
        break
    print("Invalid destination. Please select from the available options.")

# ---------------------------
# Step 6: Show preference options
# ---------------------------
preferences_list = ["Cheap", "Fast", "Comfortable", "Balanced"]
print(f"Preference options: {', '.join(preferences_list)}")
while True:
    preference = input("Enter your travel preference: ").strip()
    if preference.capitalize() in preferences_list:
        preference = preference.capitalize()
        break
    print("Invalid preference. Choose from the list above.")

# ---------------------------
# Step 7: Filter routes by source, destination
# ---------------------------
possible_routes = [r for r in routes if r['source'] == source and r['destination'] == destination]
if not possible_routes:
    print(f"No routes found from {source} to {destination}.")
    exit()

# ---------------------------
# Step 8: Filter blocked cities
# ---------------------------
filtered_routes = []
for r in possible_routes:
    route_cities = [r['source']] + r.get('via', []) + [r['destination']]
    if not any(city in blocked_cities for city in route_cities):
        filtered_routes.append(r)

if not filtered_routes:
    print(f"No routes available after excluding blocked cities: {blocked_cities}")
    exit()

# ---------------------------
# Step 9: Filter by travel time
# ---------------------------
filtered_routes = [r for r in filtered_routes if r.get("travel_time", "").lower() == travel_time.lower()]
if not filtered_routes:
    print(f"No routes available for {travel_time} travel.")
    exit()

# ---------------------------
# Step 10: Calculate totals
# ---------------------------
for r in filtered_routes:
    r['total_cost'] = r['cost']
    r['total_time'] = r['time']
    r['mode_switches'] = r['switches']
    r['path'] = [r['source']] + r.get('via', []) + [r['destination']]
    r['modes'] = [r['mode']]

# ---------------------------
# Step 11: Select best route
# ---------------------------
if preference.lower() == "cheap":
    best_route = min(filtered_routes, key=lambda x: x['total_cost'])
elif preference.lower() == "fast":
    best_route = min(filtered_routes, key=lambda x: x['total_time'])
elif preference.lower() == "comfortable":
    best_route = min(filtered_routes, key=lambda x: x['mode_switches'])
elif preference.lower() == "balanced":
    best_route = min(filtered_routes, key=lambda x: x['total_cost'] + x['total_time'])
else:
    best_route = filtered_routes[0]

# ---------------------------
# Step 12: Print detailed plan
# ---------------------------
print("\n===== SMART TRAVEL PLAN =====")
print(f"Persona: {persona}")
print(f"Travel Time: {travel_time}")
print(f"Blocked Cities: {blocked_cities}")
print(f"Source: {source}")
print(f"Destination: {destination}")
print(f"Preference: {preference}")

print("\n===== ALL POSSIBLE ROUTES =====")
for idx, r in enumerate(filtered_routes, start=1):
    print(f"\nRoute {idx}:")
    print(f"  Path: {' → '.join(r['path'])}")
    print(f"  Cost: {r['total_cost']}")
    print(f"  Time: {r['total_time']} hours")
    print(f"  Distance: {r.get('distance', 'N/A')} km")
    print(f"  Mode(s): {', '.join(r['modes'])}")
    print(f"  Mode Switches: {r['mode_switches']}")

print("\n===== BEST ROUTE =====")
print(f"Path: {' → '.join(best_route['path'])}")
print(f"Cost: {best_route['total_cost']}")
print(f"Time: {best_route['total_time']} hours")
print(f"Distance: {best_route.get('distance', 'N/A')} km")
print(f"Mode(s): {', '.join(best_route['modes'])}")
print(f"Switches: {best_route['mode_switches']}")

print("\n AI Recommendation:")
print(explain_plan(best_route, preference))