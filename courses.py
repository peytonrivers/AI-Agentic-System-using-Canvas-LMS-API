def get_courses(canvas, enrollment_state="active", include_progress=True):
    """Return a list of courses for a given enrollment state."""
    params = {
        "enrollment_state": enrollment_state,
    }

    if include_progress:
        params["include[]"] = ["course_progress"]

    return canvas.get("courses", params=params)

def list_clean_courses(canvas):
    """Return a list of clean courses."""
    raw = get_courses(canvas)

    cleaned = []
    for c in raw:
        cleaned.append({
            "id": c["id"],
            "name": c["name"],
            "course_code": c.get("course_code"),
            "workflow_state": c.get("workflow_state"),
            "start_at": c.get("start_at"),
            "end_at": c.get("end_at"),
            "default_view": c.get("default_view"),
            "course_image": c.get("course_image"),
            "syllabus_body": c.get("syllabus_body"),
            "course_progress": c.get("course_progress"),
        })
    return cleaned

def get_course_details(canvas, course_id):
    """Return details for a specific course."""
    params = {
        "include[]": [
            "syllabus_body",
            "course_progress",
            "term",
            "teachers",
            "course_image",
        ]
    }
    return canvas.get(f"courses/{course_id}", params=params)

def get_course_progress(canvas, course_id, user_id="self"):
    """Return progress for a specific course and user."""
    return canvas.get(f"courses/{course_id}/users/{user_id}/progress")