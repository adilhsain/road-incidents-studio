from flask import Flask, render_template, request, jsonify
from app.db import execute_query, test_connection

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-key"

@app.route("/")
def index():
    try:
        return render_template("mission.html")
    except Exception as e:
        return jsonify({"error": "Failed to render page", "details": str(e), "data": []}), 500

@app.route("/mission")
def mission():
    try:
        return render_template("mission.html")
    except Exception as e:
        return jsonify({"error": "Failed to render page", "details": str(e), "data": []}), 500

@app.route("/people")
def people():
    try:
        return render_template("people.html")
    except Exception as e:
        return jsonify({"error": "Failed to render page", "details": str(e), "data": []}), 500

@app.route("/deep-analysis")
def deep_analysis():
    try:
        return render_template("deep_people.html")
    except Exception as e:
        return jsonify({"error": "Failed to render page", "details": str(e), "data": []}), 500


@app.route('/api/health')
def api_health():
    try:
        db_ok = test_connection()
        return jsonify({"status": "ok", "db_connected": bool(db_ok)})
    except Exception as e:
        return jsonify({"status": "error", "db_connected": False, "error": str(e)}), 500

@app.route("/api/team-members")
def api_team_members():
    try:
        query = "SELECT member_id, full_name, student_number, role FROM team_members ORDER BY member_id"
        results = execute_query(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": "Failed to load team members", "details": str(e), "data": []}), 500

@app.route("/api/personas")
def api_personas():
    try:
        query = "SELECT persona_id, name, age, occupation, background, goals, pain_points, assigned_student, image_url FROM personas ORDER BY persona_id"
        results = execute_query(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": "Failed to load personas", "details": str(e), "data": []}), 500

@app.route("/api/people-summary")
def api_people_summary():
    injury_level = request.args.get("injury_level")
    age_group = request.args.get("age_group")
    road_user_type = request.args.get("road_user_type")
    try:
        base_query = (
            "SELECT \n"
            "  COALESCE(p.ROAD_USER_TYPE, 'Unknown') AS road_user_type,\n"
            "  COALESCE(p.INJ_LEVEL, 'Unknown') AS inj_level,\n"
            "  COUNT(*) AS total_people,\n"
            "  SUM(CASE WHEN p.TAKEN_HOSPITAL = 'Yes' THEN 1 ELSE 0 END) AS hospital_count,\n"
            "  SUM(CASE WHEN p.EJECTED_CODE NOT IN ('Not ejected', '0') THEN 1 ELSE 0 END) AS ejected_count\n"
            "FROM PERSON p\n"
            "JOIN ACCIDENT a ON p.ACCIDENT_NO = a.ACCIDENT_NO\n"
            "WHERE 1=1\n"
        )

        conditions = []
        params = []

        if injury_level and injury_level != 'All':
            conditions.append("AND p.INJ_LEVEL = ?")
            params.append(injury_level)
        if age_group and age_group != 'All':
            conditions.append("AND p.AGE_GROUP = ?")
            params.append(age_group)
        if road_user_type and road_user_type != 'All':
            conditions.append("AND p.ROAD_USER_TYPE = ?")
            params.append(road_user_type)

        if conditions:
            base_query += " " + " ".join(conditions) + "\n"

        base_query += (
            "GROUP BY p.ROAD_USER_TYPE, p.INJ_LEVEL\n"
            "ORDER BY total_people DESC"
        )

        results = execute_query(base_query, params)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": "Failed to load people summary", "details": str(e), "data": []}), 500

@app.route("/api/deep-analysis")
def api_deep_analysis():
    try:
        injury_type = (request.args.get("injury_type") or "all").lower()

        outer_conditions = []
        inner_conditions = []

        if injury_type == 'fatal':
            outer_conditions.append("p.INJ_LEVEL = 'Fatal'")
            inner_conditions.append("p2.INJ_LEVEL = 'Fatal'")
        elif injury_type == 'serious':
            outer_conditions.append("p.INJ_LEVEL = 'Serious Injury'")
            inner_conditions.append("p2.INJ_LEVEL = 'Serious Injury'")

        outer_where = ("WHERE " + " AND ".join(outer_conditions)) if outer_conditions else ""
        inner_where = ("WHERE " + " AND ".join(inner_conditions)) if inner_conditions else ""

        # Use the nested query from level3_b.sql structure
        query = (
            "SELECT p.AGE_GROUP AS age_group, p.ROAD_USER_TYPE AS road_user_type, p.INJ_LEVEL AS inj_level, COUNT(*) AS incident_count "
            "FROM PERSON p "
            "JOIN ACCIDENT a USING (ACCIDENT_NO) "
            f"{outer_where} "
            "GROUP BY p.AGE_GROUP, p.ROAD_USER_TYPE, p.INJ_LEVEL "
            "HAVING COUNT(*) > ("
            "  SELECT AVG(group_count) FROM ("
            "    SELECT COUNT(*) AS group_count "
            "    FROM PERSON p2 "
            "    JOIN ACCIDENT a2 USING (ACCIDENT_NO) "
            f"{inner_where} "
            "    GROUP BY p2.AGE_GROUP, p2.ROAD_USER_TYPE, p2.INJ_LEVEL"
            "  ) AS avg_table"
            ") "
            "ORDER BY incident_count DESC "
            "LIMIT 20"
        )

        rows = execute_query(query)

        # add rank
        for idx, row in enumerate(rows, start=1):
            row['rank'] = idx

        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": "Failed to run deep analysis", "details": str(e), "data": []}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
