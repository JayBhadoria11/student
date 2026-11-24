from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-this-for-production"

# Sample data: replace these details with actual student information.
student = {
    "name": "Aarav Sharma",
    "roll": "MITS2026AI014",
    "enrollment": "0827AI241014",
    "course": "B.Tech - Artificial Intelligence",
    "semester": "Semester 3",
    "year": "2026-27",
    "email": "aarav.sharma@example.com",
    "phone": "+91 98765 43210",
    "batch": "2024-2028",
    "advisor": "Dr. Ananya Verma",
}

subjects = [
    {"name": "Mathematics for AI", "code": "AI301", "credits": 4, "marks": 86, "grade": "A"},
    {"name": "Data Structures", "code": "CS302", "credits": 4, "marks": 91, "grade": "A+"},
    {"name": "Digital Logic", "code": "EC303", "credits": 3, "marks": 78, "grade": "B+"},
    {"name": "Python Programming", "code": "AI304", "credits": 4, "marks": 94, "grade": "A+"},
    {"name": "Professional Communication", "code": "HS305", "credits": 2, "marks": 82, "grade": "A"},
]

attendance = [
    {"subject": "Mathematics for AI", "held": 40, "present": 36},
    {"subject": "Data Structures", "held": 42, "present": 39},
    {"subject": "Digital Logic", "held": 36, "present": 30},
    {"subject": "Python Programming", "held": 44, "present": 41},
    {"subject": "Professional Communication", "held": 30, "present": 27},
]

achievements = [
    {"title": "Python Programming Fundamentals", "type": "Course completion", "date": "12 Sep 2026", "icon": "✦"},
    {"title": "Inter-college Coding Challenge", "type": "Participation", "date": "03 Aug 2026", "icon": "⌘"},
    {"title": "Department Project Showcase", "type": "Merit recognition", "date": "18 Jul 2026", "icon": "★"},
]

feedback = [
    {"teacher": "Dr. Ananya Verma", "subject": "Mathematics for AI", "date": "15 Nov 2026",
     "message": "You show good conceptual understanding. Keep practising problem-solving steps and explaining your reasoning clearly."},
    {"teacher": "Prof. R. Mehta", "subject": "Python Programming", "date": "10 Nov 2026",
     "message": "Consistent improvement in practical work. Try writing more modular code and adding test cases to your programs."},
]

def grade_from_marks(marks):
    if marks >= 90:
        return "A+", 10
    elif marks >= 80:
        return "A", 9
    elif marks >= 70:
        return "B+", 8
    elif marks >= 60:
        return "B", 7
    elif marks >= 50:
        return "C", 6
    elif marks >= 40:
        return "D", 5
    else:
        return "F", 0

def calculate_cgpa():
    total_points = 0
    total_credits = 0
    for subject in subjects:
        _, point = grade_from_marks(subject["marks"])
        total_points += point * subject["credits"]
        total_credits += subject["credits"]
    return round(total_points / total_credits, 2) if total_credits else 0

def attendance_percentage(item):
    if item["held"] == 0:
        return 0
    return round(item["present"] / item["held"] * 100, 1)

@app.route("/")
def dashboard():
    total_held = sum(item["held"] for item in attendance)
    total_present = sum(item["present"] for item in attendance)
    overall_attendance = round(total_present / total_held * 100, 1) if total_held else 0
    return render_template("dashboard.html", student=student, cgpa=calculate_cgpa(),
                           attendance=overall_attendance, subjects=subjects,
                           achievements=achievements[:2])

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        student["name"] = request.form.get("name", student["name"]).strip() or student["name"]
        student["email"] = request.form.get("email", student["email"]).strip()
        student["phone"] = request.form.get("phone", student["phone"]).strip()
        flash("Profile details updated.")
        return redirect(url_for("profile"))
    return render_template("profile.html", student=student)

@app.route("/academics")
def academics():
    total = sum(s["marks"] for s in subjects)
    percentage = round(total / (len(subjects) * 100) * 100, 1) if subjects else 0
    return render_template("academics.html", subjects=subjects, cgpa=calculate_cgpa(),
                           total=total, percentage=percentage)

@app.route("/attendance")
def attendance_page():
    rows = []
    for item in attendance:
        rows.append({**item, "percentage": attendance_percentage(item)})
    total_held = sum(item["held"] for item in attendance)
    total_present = sum(item["present"] for item in attendance)
    overall = round(total_present / total_held * 100, 1) if total_held else 0
    return render_template("attendance.html", rows=rows, overall=overall)

@app.route("/teacher", methods=["GET", "POST"])
def teacher_page():
    if request.method == "POST":
        try:
            updated_marks = []
            updated_attendance = []
            for i, subject in enumerate(subjects):
                marks = int(request.form.get(f"marks_{i}", subject["marks"]))
                held = int(request.form.get(f"held_{i}", attendance[i]["held"]))
                present = int(request.form.get(f"present_{i}", attendance[i]["present"]))
                if not 0 <= marks <= 100:
                    raise ValueError("Marks must be between 0 and 100.")
                if held < 0 or present < 0 or present > held:
                    raise ValueError("Attendance must have valid class counts, with present not greater than held.")
                updated_marks.append((marks, grade_from_marks(marks)[0]))
                updated_attendance.append((held, present))

            # Update the shared records used by both teacher and student pages.
            for i, (marks, grade) in enumerate(updated_marks):
                subjects[i]["marks"] = marks
                subjects[i]["grade"] = grade
            for i, (held, present) in enumerate(updated_attendance):
                attendance[i]["held"] = held
                attendance[i]["present"] = present
            flash("Marks and attendance saved. Student pages now show the updated records.")
        except ValueError as error:
            flash(str(error) or "Please enter valid whole numbers.")
        return redirect(url_for("teacher_page"))

    rows = []
    for i, subject in enumerate(subjects):
        rows.append({**subject, "held": attendance[i]["held"], "present": attendance[i]["present"]})
    return render_template("teacher.html", student=student, rows=rows)

@app.route("/achievements")
def achievements_page():
    return render_template("achievements.html", achievements=achievements)

@app.route("/feedback")
def feedback_page():
    return render_template("feedback.html", feedback=feedback)

@app.route("/marksheet")
def marksheet():
    total = sum(s["marks"] for s in subjects)
    maximum = len(subjects) * 100
    percentage = round(total / maximum * 100, 2) if maximum else 0
    return render_template("marksheet.html", student=student, subjects=subjects,
                           total=total, maximum=maximum, percentage=percentage,
                           cgpa=calculate_cgpa())

if __name__ == "__main__":
    app.run(debug=True, port=5001)
