from flask import Flask, render_template, request, jsonify
from app.db import execute_query, test_connection
import logging

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-key"
logging.basicConfig(level=logging.INFO)

def respond_error(message, status_code=500):
    return jsonify({"error": message, "data": []}), status_code

@app.route("/")
def index():
    try:
        return render_template("mission.html")
    except Exception as error:
        logging.exception("Failed to render mission page.")
        return respond_error("Unable to load mission page.")

@app.route("/mission")
def mission():
    try:
        return render_template("mission.html")
    except Exception as error:
        logging.exception("Failed to render mission page.")
        return respond_error("Unable to load mission page.")

@app.route("/people")
def people():
    try:
        return render_template("people.html")
    except Exception as error:
        logging.exception("Failed to render people page.")
        return respond_error("Unable to load people page.")

@app.route("/deep-analysis")
def deep_analysis():
    try:
        return render_template("deep_people.html")
    except Exception as error:
        logging.exception("Failed to render deep analysis page.")
        return respond_error("Unable to load deep analysis page.")

@app.route("/api/health")
def api_health():
    try:
        return jsonify({"status": "ok", "db_connected": test_connection()})
    except Exception as error:
        logging.exception("Health check failed.")
        return respond_error("Health check failed.")

@app.route("/api/team-members")
def api_team_members():
    try:
        query = "SELECT member_id, full_name, student_number, role FROM team_members"
        results = execute_query(query)
        return jsonify({"error": None, "data": results})
    except Exception as error:
        logging.exception("Failed to fetch team members.")
        return respond_error("Unable to retrieve team members.")

@app.route("/api/personas")
def api_personas():
    try:
        query = "SELECT persona_id, name, age, occupation, background, goals, pain_points, assigned_student, image_url FROM personas"
        results = execute_query(query)
        return jsonify({"error": None, "data": results})
    except Exception as error:
        logging.exception("Failed to fetch personas.")
        return respond_error("Unable to retrieve personas.")

@app.route("/api/people-summary")
def api_people_summary():
    try:
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
        return jsonify({"error": None, "data": results})
    except Exception as error:
        logging.exception("Failed to fetch people summary.")
        return respond_error("Unable to retrieve people summary.")

@app.route("/api/deep-analysis")
def api_deep_analysis():
    try:
        injury_type = request.args.get("injury_type")
        if not injury_type:
            return respond_error("Missing required query parameter: injury_type", 400)

        query = (
            "SELECT p.ROAD_USER_TYPE, COUNT(*) AS incident_count, "
            "SUM(CASE WHEN a.SPEED_ZONE IS NOT NULL THEN 1 ELSE 0 END) AS speed_zone_records "
            "FROM PERSON p "
            "JOIN ACCIDENT a ON p.ACCIDENT_NO = a.ACCIDENT_NO "
            "WHERE p.INJ_LEVEL = ? "
            "GROUP BY p.ROAD_USER_TYPE"
        )

        results = execute_query(query, [injury_type])
        return jsonify({"error": None, "data": results})
    except Exception as error:
        logging.exception("Failed to fetch deep analysis.")
        return respond_error("Unable to retrieve deep analysis.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
