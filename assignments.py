from dates import is_overdue

def get_assignments(canvas, course_id: int):
    """Return all assignments for a given course."""
    return canvas.get(f"courses/{course_id}/assignments")

def list_clean_assignments(canvas, course_id):
    """Return a list of clean assignments for a given course."""
    raw = canvas.get(f"courses/{course_id}/assignments")  

    cleaned = []
    for a in raw:
        s = a.get("submission", {})
        cleaned.append({
            "id": a["id"],
            "name": a["name"],
            "due_at": a["due_at"],
            "points_possible": a.get("points_possible"),
            "score": s.get("score"),
            "late": s.get("late"),
            "missing": s.get("missing"),
            "percentage": (s["score"] / a["points_possible"] * 100)
                         if s.get("score") is not None and a.get("points_possible")
                         else None,
            "html_url": a.get("html_url"),
        })
    return cleaned

def get_overdue(canvas, course_id):
    """Return a list of overdue assignments for a given course."""
    assignments = list_clean_assignments(canvas, course_id)
    return [a for a in assignments if is_overdue(a["due_at"])]


def get_grades(canvas, course_id):
    """Return assignment id, name, grades, points possible, percent, and """
    url = f"courses/{course_id}/students/submissions"
    params = {
        "student_ids[]": "self",
        "include[]": ["assignment", "total_scores", "rubric"],
        "per_page": 100
    }
    data = canvas.get(url, params=params)
    grades = []
    for a in data:
        assignment = a.get("assignment", {})
        total_scores = a.get("total_scores", {})
        rubric = a.get("rubric")
        score = a.get("score")
        points = a.get("points_possible")
        final_info = {
            "assignment_id": assignment.get("id"),
            "name": assignment.get("name"),
            "description": (assignment.get("description")) if (assignment.get("description") is not None) else None,
            "score": score,
            "points_possible": points,
            "percent": (score / points * 100) if (score and points is not None) else None,
            "rubric": rubric,
            "html_url": assignment.get("html_url")
            }
        grades.append(final_info)
    return grades

def get_weak_grades(canvas, course_id, threshold=80):
    """Return a list of weak grades for a given course."""
    lower = get_grades(canvas, course_id)
    return [
        a for a in lower if a["percent"] is not None and a["percent"] < threshold
    ]

def get_strong_grades(canvas, course_id, threshold=80):
    strong = get_grades(canvas, course_id)
    return [
        a for a in strong if a["percent"] is not None and a["percent"] >= threshold
    ]
def get_current_grade(canvas, course_id):
    url = f"courses/{course_id}/enrollments"
    params = {
        "user_id": "self",
        "include[]": "total_scores",
        "per_page": 100,
    }
    data = canvas.get(url, params=params)
    final = []
    for a in data:
        grades = a.get("grades", {})
        course_info = {
            "course_id": a.get("course_id"),
            "current_grade": grades.get("current_score") if (grades.get("current_score") is not None) else None
            }
        final.append(course_info)
    return final