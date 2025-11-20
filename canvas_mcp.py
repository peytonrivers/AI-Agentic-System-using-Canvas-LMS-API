from fastmcp import FastMCP
from client import CanvasClient
from overview import get_student_overview
from assignments import (
    get_assignments,
    list_clean_assignments,
    get_weak_grades,
    get_strong_grades,
    get_overdue,
    get_grades,
    get_current_grade
   )
from courses import (
    list_clean_courses,
    get_course_details,
    get_course_progress,
)
from modules import (
    list_clean_modules,
    list_clean_module_items,
    build_prerequisite_graph,
)
from quizzes import (
    list_clean_quizzes,
    get_quiz_details,
)
from submissions import (
    list_clean_submissions,
    get_assignment_submissions,
    get_submission,
)

mcp = FastMCP("canvas-mcp")

canvas = CanvasClient()

@mcp.tool
def overview():
    """Return upcoming assignments across all active courses."""
    return get_student_overview(canvas)

@mcp.tool
def class_grades(course_id: int):
    """Return grades for a specific class"""
    return get_grades(canvas, course_id)

@mcp.tool
def assignments(course_id: int):
    """Return assignments for a specific course."""
    return get_assignments(canvas, course_id)

@mcp.tool
def clean_assignments(course_id: int):
    """Return clean assignments for a specific course."""
    return list_clean_assignments(canvas, course_id)

@mcp.tool
def current_total_grade(course_id: int):
    """Returning the current course grade"""
    return get_current_grade(canvas, course_id)

@mcp.tool
def weak_grades(course_id: int):
    """Return weak grades for a specific course."""
    return get_weak_grades(canvas, course_id)

@mcp.tool
def strong_grades(course_id: int):
    """Return strong grades for a specific course."""
    return get_strong_grades(canvas, course_id)

@mcp.tool
def overdue(course_id: int):
    """Return overdue assignments for a specific course."""
    return get_overdue(canvas, course_id)

@mcp.tool
def courses():
    """List all active courses for the current user."""
    return list_clean_courses(canvas)

@mcp.tool
def course_details(course_id: int):
    """Return detailed info about a specific course."""
    return get_course_details(canvas, course_id)

@mcp.tool
def course_progress(course_id: int):
    """Return progress info for the current user in this course."""
    return get_course_progress(canvas, course_id)

@mcp.tool
def modules(course_id: int):
    """Return clean module metadata."""
    return list_clean_modules(canvas, course_id)

@mcp.tool
def module_items(course_id: int, module_id: int):
    """Return clean module items for this module."""
    return list_clean_module_items(canvas, course_id, module_id)

@mcp.tool
def prereq_graph(course_id: int):
    """Return module prerequisite graph for course flow analysis."""
    return build_prerequisite_graph(canvas, course_id)

@mcp.tool
def quizzes(course_id: int):
    """Return cleaned list of quizzes for this course."""
    return list_clean_quizzes(canvas, course_id)

@mcp.tool
def quiz_details(course_id: int, quiz_id: int):
    """Return cleaned details for a single quiz."""
    return get_quiz_details(canvas, course_id, quiz_id)

@mcp.tool
def submissions(course_id: int):
    """Return cleaned submissions for the current user."""
    return list_clean_submissions(canvas, course_id)

@mcp.tool
def assignment_submissions(course_id: int, assignment_id: int):
    """Return submissions for a single assignment."""
    return get_assignment_submissions(canvas, course_id, assignment_id)

@mcp.tool
def submission(course_id: int, assignment_id: int, user_id: int):
    """Return a single submission."""
    return get_submission(canvas, course_id, assignment_id, user_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")