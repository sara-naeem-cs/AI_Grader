from fastapi import APIRouter, File, UploadFile

from utils.pdf_extract_text import extract_text, extract_rubric
from utils.text_limit import size_limit_assignment, size_limit_rubric

from services.grading_service import grade_assignment

router = APIRouter()

@router.post("/grade")
async def submit(assignment: UploadFile = File(...), rubric: UploadFile = File(...)):

    # Extract text directly from uploaded file objects (no temp file needed)
    assignment_text = extract_text(assignment.file)
    # Returns a string with text or an array of arrays.
    rubric_text = extract_rubric(rubric.file)

    # Limit number of characters:
    assignment_text = size_limit_assignment(assignment_text)
    rubric_text = size_limit_rubric(rubric_text)

    response = grade_assignment(assignment_text, rubric_text)

    # Return following JSON
    return {
        "assignment_filename": assignment.filename,
        "rubric_filename": rubric.filename,
        "message": "received",
        "response": response
    }
