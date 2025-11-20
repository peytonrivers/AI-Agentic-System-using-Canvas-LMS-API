def get_modules(canvas, course_id, include_items=True):
    """Return a list of modules for a given course."""
    params = {}
    if include_items:
        params["include[]"] = ["items", "content_details"]

    return canvas.get(f"courses/{course_id}/modules", params=params)

def list_clean_modules(canvas, course_id):
    """Return a list of clean modules for a given course."""
    raw = get_modules(canvas, course_id)

    cleaned = []
    for m in raw:
        cleaned.append({
            "id": m["id"],
            "name": m["name"],
            "position": m["position"],
            "unlock_at": m.get("unlock_at"),
            "workflow_state": m.get("workflow_state"),
            "items_count": m.get("items_count"),
            "require_sequential_progress": m.get("require_sequential_progress"),
            "prerequisite_module_ids": m.get("prerequisite_module_ids"),
            "state": m.get("state"),
            "completed_at": m.get("completed_at"),
        })
    return cleaned

def get_module_items(canvas, course_id, module_id, include_content=True):
    """Return a list of items for a given module."""
    params = {}
    if include_content:
        params["include[]"] = ["content_details"]

    return canvas.get(f"courses/{course_id}/modules/{module_id}/items", params=params)

def list_clean_module_items(canvas, course_id, module_id):
    """Return a list of clean items for a given module."""
    raw = get_module_items(canvas, course_id, module_id)

    cleaned = []
    for it in raw:
        cd = it.get("content_details", {})
        cleaned.append({
            "id": it["id"],
            "module_id": it["module_id"],
            "title": it["title"],
            "type": it["type"],
            "position": it["position"],
            "content_id": it.get("content_id"),
            "html_url": it.get("html_url"),
            "url": it.get("url"),
            "completion_requirement": it.get("completion_requirement"),
            "points_possible": cd.get("points_possible"),
            "due_at": cd.get("due_at"),
            "unlock_at": cd.get("unlock_at"),
            "lock_at": cd.get("lock_at"),
        })
    return cleaned

def build_prerequisite_graph(canvas, course_id):
    """Build a prerequisite graph for a given course."""
    modules = get_modules(canvas, course_id, include_items=False)
    graph = {}

    for m in modules:
        graph[m["id"]] = m.get("prerequisite_module_ids", [])

    return graph
