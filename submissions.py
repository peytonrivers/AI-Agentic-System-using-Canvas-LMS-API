def get_all_submissions(canvas, course_id):
    """
    Returns all submissions for the current user across all assignments.
    """
    params = {
        "student_ids[]": "self",
        "include[]": ["submission_comments", "user"]
    }
    return canvas.get(f"courses/{course_id}/students/submissions", params=params)

def list_clean_submissions(canvas, course_id):
    """Return a list of clean submissions for a given course."""
    raw = get_all_submissions(canvas, course_id)

    cleaned = []
    for s in raw:
        cleaned.append({
            "assignment_id": s.get("assignment_id"),
            "user_id": s.get("user_id"),
            "attempt": s.get("attempt"),
            "submitted_at": s.get("submitted_at"),
            "score": s.get("score"),
            "grade": s.get("grade"),
            "late": s.get("late"),
            "workflow_state": s.get("workflow_state"),
            "submission_type": s.get("submission_type"),
            "body": s.get("body"),
            "url": s.get("url"),
            "html_url": s.get("html_url"),
            "preview_url": s.get("preview_url"),
            "grade_matches_current_submission": s.get("grade_matches_current_submission"),
            "assignment_visible": s.get("assignment_visible"),
        })
    return cleaned

def get_assignment_submissions(canvas, course_id, assignment_id):
    """Return submissions for a specific assignment."""
    params = {
        "student_ids[]": "self",
        "include[]": ["submission_comments"]
    }

    return canvas.get(
        f"courses/{course_id}/assignments/{assignment_id}/submissions",
        params=params
    )

def get_submission(canvas, course_id, assignment_id, user_id):
    """Return a single submission."""
    return canvas.get(f"courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}")