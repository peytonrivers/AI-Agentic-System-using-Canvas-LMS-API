def get_student_overview(canvas):
    """Return active courses and their upcoming assignments."""
    courses = canvas.get("courses?enrollment_state=active")
    overview = []

    for c in courses:
        course_id = c.get("id")
        if not course_id:
            continue
        assignments = canvas.get(f"courses/{course_id}/assignments?bucket=upcoming")
        overview.append({
            "course": c.get("name"),
            "upcoming": [
                {"name": a.get("name"), "due_at": a.get("due_at")}
                for a in assignments if a.get("due_at")
            ]
        })
    return overview