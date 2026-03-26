from pathlib import Path

from flask import Flask, jsonify, request

from advanced_features import apply_delay, apply_switching_penalty
from auth import login_user, register_user, verify_token
from constraints import filter_plans
from explainer import explain_plan
from persona import get_preference_from_persona
from planner import build_plan
from preferences import choose_best_plan
from search import dijkstra
from utils import load_graph

app = Flask(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ROUTES_FILE = DATA_DIR / "routes.csv"
graph = load_graph(ROUTES_FILE)


@app.get("/health")
def health():
    return jsonify({"ok": True})


# ---------------- AUTH APIs ---------------- #
@app.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if register_user(username, password):
        return jsonify({"msg": "User registered successfully"})
    return jsonify({"msg": "User already exists or invalid input"}), 400


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    token = login_user(username, password)
    if token:
        return jsonify({"token": token})
    return jsonify({"msg": "Invalid credentials"}), 401


# ---------------- ROUTE PLANNER API ---------------- #
@app.post("/plan")
def plan():
    user = verify_token(request.headers.get("Authorization"))
    if not user:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json(silent=True) or {}

    source = data.get("source")
    destination = data.get("destination")
    if not source or not destination:
        return jsonify({"msg": "source and destination are required"}), 400

    persona = (data.get("persona") or "").strip().lower() or None
    preference = (data.get("preference") or "").strip().lower() or None
    travel_time = (data.get("travel_time") or "").strip().lower() or None  # day/night
    blocked_cities = data.get("blocked_cities") or data.get("blocked") or []

    if isinstance(blocked_cities, str):
        blocked_cities = [c.strip() for c in blocked_cities.split(",") if c.strip()]

    constraints = data.get("constraints") or {}
    if not isinstance(constraints, dict):
        constraints = {}

    # Persona -> preference fallback (student/business/tourist/eco)
    if not preference and persona:
        preference = get_preference_from_persona(persona)
    preference = preference or "cheap"

    # Merge route-related constraints
    constraints = dict(constraints)
    if blocked_cities:
        constraints["avoid_cities"] = blocked_cities
    if travel_time:
        constraints["travel_time"] = travel_time

    allowed_modes = constraints.get("preferred_mode")
    if isinstance(allowed_modes, str) and allowed_modes.strip():
        allowed_modes = [allowed_modes.strip()]

    # Candidate set from different optimization weights; ranking handles comfortable/balanced.
    plans = []
    for weight in ("cost", "time", "distance"):
        _, path = dijkstra(
            graph,
            source,
            destination,
            weight,
            avoid_cities=constraints.get("avoid_cities"),
            travel_time=constraints.get("travel_time"),
            allowed_modes=allowed_modes,
        )
        if not path:
            continue
        plans.append(build_plan(graph, path))

    plans = filter_plans(plans, constraints)
    if not plans:
        return jsonify({"msg": "No route found for the given inputs"}), 404

    apply_switch_penalty = bool(data.get("apply_switch_penalty", False))
    switching_penalty = int(data.get("switching_penalty", 50))
    if apply_switch_penalty:
        plans = [apply_switching_penalty(p, penalty=switching_penalty) for p in plans]

    best_plan, top_plans = choose_best_plan(plans, preference=preference, top_n=3)
    if not best_plan:
        return jsonify({"msg": "No route found for the given inputs"}), 404

    simulate_delay = bool(data.get("simulate_delay", False))
    if simulate_delay:
        best_plan = apply_delay(best_plan)

    return jsonify(
        {
            "user": user,
            "inputs": {
                "source": source,
                "destination": destination,
                "persona": persona,
                "preference": preference,
                "travel_time": travel_time,
                "blocked_cities": blocked_cities,
                "constraints": constraints,
            },
            "best_route": best_plan,
            "top_routes": top_plans,
            "explanation": explain_plan(best_plan, preference),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
