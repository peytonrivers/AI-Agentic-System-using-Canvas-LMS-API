import datetime
def is_overdue(due_at):
    """Check if a due date is overdue."""
    if not due_at:
        return False
    due_date = datetime.fromisoformat(due_at.replace('Z', '+00:00'))
    return due_date < datetime.now(due_date.tzinfo)