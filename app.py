from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# GPA Quality Points Mapping
GRADE_POINTS = {
    "A": 12, "A-": 11, "B+": 10, "B": 9, "B-": 8,
    "C+": 7, "C": 6, "C-": 5, "D": 3, "E": 0
}

@app.route('/calculate_gpa', methods=['POST'])
def calculate_gpa():
    data = request.json
    terms = data.get("terms", {})

    if not terms:
        return jsonify({"error": "No terms provided"}), 400

    total_quality_points = 0
    total_gpa_hours = 0
    term_gpas = {}

    two_course_terms = 0
    four_course_terms = 0

    for term, grades in terms.items():
        if grades == "Off-Term":
            term_gpas[term] = "Off-Term"
            continue

        if not grades or len(grades) < 2:
            term_gpas[term] = "Invalid (Must have at least 2 courses)"
            continue

        if len(grades) == 2:
            two_course_terms += 1
        if len(grades) == 4:
            four_course_terms += 1

        term_quality_points = sum(GRADE_POINTS.get(grade, 0) for grade in grades)
        term_gpa_hours = len(grades)

        term_gpa = round((term_quality_points / term_gpa_hours) / 3, 2)
        term_gpas[term] = term_gpa

        total_quality_points += term_quality_points
        total_gpa_hours += term_gpa_hours

    # Enforce term limits
    if two_course_terms > 3:
        return jsonify({"error": "You can only have a maximum of 3 two-course terms"}), 400
    if four_course_terms > 4:
        return jsonify({"error": "You can only have a maximum of 4 four-course terms"}), 400

    # Calculate cumulative GPA
    cumulative_gpa = round((total_quality_points / total_gpa_hours) / 3, 2) if total_gpa_hours > 0 else 0

    return jsonify({
        "term_gpas": term_gpas,
        "cumulative_gpa": cumulative_gpa
    })

if __name__ == '__main__':
    app.run(debug=True)
