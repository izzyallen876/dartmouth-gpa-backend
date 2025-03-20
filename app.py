from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# ✅ **Health check route to prevent "Not Found" error**
@app.route('/')
def home():
    return "Hello from Flask! API is live.", 200

# ✅ **GPA Calculation API**
@app.route('/calculate_gpa', methods=['POST'])
def calculate_gpa():
    data = request.json
    if not data or "terms" not in data:
        return jsonify({"error": "Missing data"}), 400

    terms = data["terms"]
    quality_points = 0
    total_courses = 0

    grade_mapping = {
        "A": 12, "A-": 11, "B+": 10, "B": 9, "B-": 8,
        "C+": 7, "C": 6, "C-": 5, "D": 3, "E": 0
    }

    term_gpas = {}

    for term, grades in terms.items():
        term_qp = sum(grade_mapping.get(grade, 0) for grade in grades)
        term_courses = len(grades)
        if term_courses > 0:
            term_gpas[term] = round((term_qp / term_courses) / 3, 2)
            quality_points += term_qp
            total_courses += term_courses

    cumulative_gpa = round((quality_points / total_courses) / 3, 2) if total_courses > 0 else 0

    return jsonify({"cumulative_gpa": cumulative_gpa, "term_gpas": term_gpas})

# ✅ **Ensure Render uses the correct port**
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render's environment variable
    app.run(host='0.0.0.0', port=port)
