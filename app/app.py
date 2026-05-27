from flask import Flask, render_template, request, jsonify
from app.db import execute_query

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-key"

@app.route("/")
def index():
    return render_template("mission.html")

@app.route("/mission")
def mission():
    return render_template("mission.html")

@app.route("/people")
def people():
    return render_template("people.html")

@app.route("/deep-analysis")
def deep_analysis():
    return render_template("deep_people.html")

@app.route("/api/team-members")
def api_team_members():
    query = "SELECT member_id, full_name, student_number, role FROM team_members"
    results = execute_query(query)
    return jsonify(results)

@app.route("/api/personas")
def api_personas():
    query = "SELECT persona_id, name, age, occupation, background, goals, pain_points, assigned_student, image_url FROM personas"
    results = execute_query(query)
    return jsonify(results)

@app.route("/api/people-summary")
def api_people_summary():
    injury_level = request.args.get("injury_level")
    age_group = request.args.get("age_group")
    road_user_type = request.args.get("road_user_type")

    base_query = "SELECT PERSON_ID, ACCIDENT_NO, SEX, AGE_GROUP, SEATING_POSITION, ROAD_USER_TYPE, HELMET_BELT_WORN, EJECTED_CODE, TAKEN_HOSPITAL, PROT_FACTOR, INJ_LEVEL, LICENCE_STATE FROM PERSON"
    conditions = []
    params = []

    if injury_level:
        conditions.append("INJ_LEVEL = ?")
        params.append(injury_level)
    if age_group:
        conditions.append("AGE_GROUP = ?")
        params.append(age_group)
    if road_user_type:
        conditions.append("ROAD_USER_TYPE = ?")
        params.append(road_user_type)

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    results = execute_query(base_query, params)
    return jsonify(results)

@app.route("/api/deep-analysis")
def api_deep_analysis():
    injury_type = request.args.get("injury_type")
    if not injury_type:
        return jsonify({"error": "Missing required query parameter: injury_type"}), 400

    query = (
        "SELECT p.ROAD_USER_TYPE, COUNT(*) AS incident_count, "
        "SUM(CASE WHEN a.SPEED_ZONE IS NOT NULL THEN 1 ELSE 0 END) AS speed_zone_records "
        "FROM PERSON p "
        "JOIN ACCIDENT a ON p.ACCIDENT_NO = a.ACCIDENT_NO "
        "WHERE p.INJ_LEVEL = ? "
        "GROUP BY p.ROAD_USER_TYPE"
    )

    results = execute_query(query, [injury_type])
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
