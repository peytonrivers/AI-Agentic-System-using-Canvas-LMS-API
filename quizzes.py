def get_quizzes(canvas, course_id, search_term=None):
    """Return a list of quizzes for a given course."""
    params = {}
    if search_term:
        params["search_term"] = search_term

    return canvas.get(f"courses/{course_id}/quizzes", params=params)

def list_clean_quizzes(canvas, course_id):
    """Return a list of clean quizzes for a given course."""
    raw = get_quizzes(canvas, course_id)

    cleaned = []
    for q in raw:
        cleaned.append({
            "id": q["id"],
            "title": q["title"],
            "description": q.get("description"),
            "quiz_type": q.get("quiz_type"),
            "question_count": q.get("question_count"),
            "points_possible": q.get("points_possible"),
            "allowed_attempts": q.get("allowed_attempts"),
            "scoring_policy": q.get("scoring_policy"),
            "time_limit": q.get("time_limit"),
            "shuffle_answers": q.get("shuffle_answers"),
            "due_at": q.get("due_at"),
            "unlock_at": q.get("unlock_at"),
            "lock_at": q.get("lock_at"),
            "show_correct_answers": q.get("show_correct_answers"),
            "show_correct_answers_at": q.get("show_correct_answers_at"),
            "hide_correct_answers_at": q.get("hide_correct_answers_at"),
            "html_url": q.get("html_url"),
        })
    return cleaned

def get_quiz_details(canvas, course_id, quiz_id):
    """Return details for a specific quiz."""
    q = canvas.get(f"courses/{course_id}/quizzes/{quiz_id}")

    return {
        "id": q["id"],
        "title": q["title"],
        "description": q.get("description"),
        "quiz_type": q.get("quiz_type"),
        "question_count": q.get("question_count"),
        "points_possible": q.get("points_possible"),
        "allowed_attempts": q.get("allowed_attempts"),
        "scoring_policy": q.get("scoring_policy"),
        "time_limit": q.get("time_limit"),
        "shuffle_answers": q.get("shuffle_answers"),
        "due_at": q.get("due_at"),
        "unlock_at": q.get("unlock_at"),
        "lock_at": q.get("lock_at"),
        "html_url": q.get("html_url"),
        "show_correct_answers": q.get("show_correct_answers"),
        "show_correct_answers_at": q.get("show_correct_answers_at"),
        "hide_correct_answers_at": q.get("hide_correct_answers_at"),
    }