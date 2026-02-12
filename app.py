from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    # Get API key
    # api_key=os.environ.get("GROQ_API_KEY"),
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

MAX_CHARS_ASSIGNMENT = 6000
MAX_CHARS_RUBRIC = 3000


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            # checking to make sure text is not None
            if page.extract_text():
                text = text + page.extract_text()
    return text


def size_limit_assignment(assignment_text):
    if assignment_text:
        assignment_text = assignment_text[:MAX_CHARS_ASSIGNMENT]
    else:
        assignment_text = ""
    return assignment_text


def size_limit_rubric(rubric_text):
    if rubric_text:
        rubric_text = rubric_text[:MAX_CHARS_RUBRIC]
    else:
        rubric_text = ""
    return rubric_text


@app.post("/submit")
async def submit(assignment: UploadFile = File(...), rubric: UploadFile = File(...)):
    # Print filenames in the terminal
    print(f"assignment: {assignment.filename}")
    print(f"rubric: {rubric.filename}")

    # Extract text directly from uploaded file objects (no temp file needed)
    assignment_text = extract_text(assignment.file)
    rubric_text = extract_text(rubric.file)

    # Limit number of characters:
    assignment_text = size_limit_assignment(assignment_text)
    rubric_text = size_limit_rubric(rubric_text)

    prompt = f"""
    You are a teacher grading an assignment. Use the following:

    ASSIGNMENT:
    {assignment_text}

    RUBRIC:
    {rubric_text}

    You MUST follow these rules:
    - Use ONLY the provided rubric to evaluate and suggest improvements.
    - Do NOT introduce new facts, concepts, or corrections unless they are explicitly required by the rubric.
    - All suggestions MUST directly correspond to a rubric category where points were deducted and the content included in the assignment.
    - If a rubric category received full marks, do NOT suggest improvements related to it.
    - Base feedback strictly on what is written in the assignment.
    - Calculate max_points strictly from the rubric.
    - If a rubric in breakdown, if the category receives full marks, the "feedback" for that category MUST be "No feedback".
    - Do NOT provide praise, explanation, or commentary for full-mark categories.
    - First calculate the sum of all category scores.
    - Then format "total_score" as "sum_earned_points/max_points".
    - Do NOT guess or estimate totals.

    Tasks:
    1. Score the assignment strictly using the rubric.
    2. If the score is less than perfect, give up to 3 suggestions for improvement in "suggested_fixes". Otherwise, return an empty list. Each suggestion MUST reference a specific rubric category where points were lost.
    3. Determine if the assignment is written by AI, Human, or a mix of both. Return this exactly as "authored_by": "AI" | "Human" | "Mixed".
    4. Return ONLY valid JSON in this format, with proper quotes and no extra text:

    {{
    "total_score": string,  // formatted exactly like "17/20",
    "breakdown": {{
        "CategoryName": {{
        "score": number,
        "feedback": string
        }}
    }},
    "suggested_fixes": ["fix 1", "fix 2"],
    "authored_by": "Human"
    }}
    """

    response = client.responses.create(
        input=prompt,
        model="llama-3.1-8b-instant"
    )

    # print(response.output_text)

    # Return following JSON
    return {
        "assignment_filename": assignment.filename,
        "rubric_filename": rubric.filename,
        "assignment_text_preview": assignment_text,
        "rubric_text_preview": rubric_text,
        "message": "received",
        "response": response.output_text
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)


"""
- Predicted grade (mark strictly)
- Changes to make (if any)
- Plagerism Detector (percentage AI vs Human)
"""
