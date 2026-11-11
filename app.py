import os
import json
import webbrowser
import threading
from flask import Flask, render_template, request, jsonify
from ai_helper import analyze_performance, generate_study_tips

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "students.json")


# ─── Helper: load / save ────────────────────────────────────────────────────

def load_students():
    """Load student records from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_students(students):
    """Save student records to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2, ensure_ascii=False)


# ─── Helper: calculate result ────────────────────────────────────────────────

def calculate_result(marks: dict) -> tuple:
    """Return (total, average, grade) for a marks dict."""
    if not marks:
        return 0, 0.0, "F"
    values = list(marks.values())
    total = sum(values)
    average = round(total / len(values), 2)
    if average >= 85:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 60:
        grade = "C"
    elif average >= 50:
        grade = "D"
    else:
        grade = "F"
    return total, average, grade


# ─── Helper: validate student payload ────────────────────────────────────────

def validate_payload(data: dict) -> str | None:
    """Return an error string or None if valid."""
    required = ["id", "name", "class", "subjects", "marks"]
    for field in required:
        if not data.get(field) and data.get(field) != 0:
            return f"Field '{field}' is required."

    subjects = [s.strip() for s in data["subjects"].split(",") if s.strip()]
    marks_raw = [m.strip() for m in data["marks"].split(",") if m.strip()]

    if not subjects:
        return "At least one subject is required."
    if len(subjects) != len(marks_raw):
        return "Number of subjects must match number of marks."
    if len(subjects) != len(set(subjects)):
        return "Duplicate subject names are not allowed."

    for m in marks_raw:
        try:
            val = float(m)
        except ValueError:
            return f"Mark '{m}' is not a valid number."
        if not (0 <= val <= 100):
            return f"Mark '{m}' must be between 0 and 100."

    return None


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/students", methods=["GET"])
def get_students():
    students = load_students()
    return jsonify(students)


@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload."}), 400

    error = validate_payload(data)
    if error:
        return jsonify({"error": error}), 400

    students = load_students()

    # Check duplicate ID
    student_id = data["id"].strip()
    if any(s["id"].lower() == student_id.lower() for s in students):
        return jsonify({"error": f"Student ID '{student_id}' already exists."}), 409

    subjects = [s.strip() for s in data["subjects"].split(",") if s.strip()]
    marks_raw = [float(m.strip()) for m in data["marks"].split(",") if m.strip()]
    marks_dict = {subjects[i]: marks_raw[i] for i in range(len(subjects))}
    total, average, grade = calculate_result(marks_dict)

    student = {
        "id": student_id,
        "name": data["name"].strip(),
        "class": data["class"].strip(),
        "marks": marks_dict,
        "total": total,
        "average": average,
        "grade": grade,
    }
    students.append(student)
    save_students(students)
    return jsonify({"message": "Student added successfully.", "student": student}), 201


@app.route("/api/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload."}), 400

    error = validate_payload(data)
    if error:
        return jsonify({"error": error}), 400

    students = load_students()
    student = next((s for s in students if s["id"].lower() == student_id.lower()), None)
    if not student:
        return jsonify({"error": f"Student '{student_id}' not found."}), 404

    subjects = [s.strip() for s in data["subjects"].split(",") if s.strip()]
    marks_raw = [float(m.strip()) for m in data["marks"].split(",") if m.strip()]
    marks_dict = {subjects[i]: marks_raw[i] for i in range(len(subjects))}
    total, average, grade = calculate_result(marks_dict)

    student["name"] = data["name"].strip()
    student["class"] = data["class"].strip()
    student["marks"] = marks_dict
    student["total"] = total
    student["average"] = average
    student["grade"] = grade

    save_students(students)
    return jsonify({"message": "Student updated successfully.", "student": student})


@app.route("/api/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    students = load_students()
    new_list = [s for s in students if s["id"].lower() != student_id.lower()]
    if len(new_list) == len(students):
        return jsonify({"error": f"Student '{student_id}' not found."}), 404
    save_students(new_list)
    return jsonify({"message": "Student deleted successfully."})


@app.route("/api/ai/<kind>/<student_id>", methods=["POST"])
def ai_request(kind, student_id):
    students = load_students()
    student = next((s for s in students if s["id"].lower() == student_id.lower()), None)
    if not student:
        return jsonify({"error": f"Student '{student_id}' not found."}), 404

    try:
        if kind == "analyze":
            result = analyze_performance(student)
        elif kind == "tips":
            result = generate_study_tips(student)
        else:
            return jsonify({"error": f"Unknown AI request type '{kind}'."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"result": result})


# ─── Auto-open browser ────────────────────────────────────────────────────────

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    threading.Timer(1.2, open_browser).start()
    app.run(debug=False, port=5000)
