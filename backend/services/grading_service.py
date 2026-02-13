from config import client


def build_prompt(assignment_text, rubric_text):

    prompt = f"""
    You are a strict teacher grading an assignment. Use the following:

    ASSIGNMENT:
    {assignment_text}

    RUBRIC:
    {rubric_text}

    You MUST follow these rules:
    - Use ONLY the provided rubric to evaluate and suggest improvements.
    - Do NOT introduce new facts, concepts, or corrections unless they are explicitly required by the rubric.
    - All suggestions MUST directly correspond to a rubric category where points were deducted and the content included in the assignment.
    - Base feedback strictly on what is written in the assignment.
    - If a rubric category receives full marks, the "feedback" for that category MUST be "No feedback".
    - Do NOT provide praise, explanation, or commentary for full-mark categories.
    - For each category score is formated as "earned_points_for_category/max_points_for_category"
    - Calculate max_points strictly from the rubric.
    - First calculate the sum of all category scores.
    - Then format "total_score" as "sum_earned_points/max_points".
    - Do NOT guess or estimate totals.

    Tasks:
    1. Score the assignment ONLY using the rubric. 
    2. The "feedback" MUST be copied verbatim from the exact rubric level description that corresponds to the assigned score.
    3. If the score is less than perfect, give up to 3 suggestions for improvement in "suggested_fixes". Otherwise, return an empty list. Each suggestion MUST reference a specific rubric category where points were lost.
    4. Return ONLY valid JSON in this format, with proper quotes, no extra text, and no markdowns.

    {{
    "total_score": string,  // formatted exactly like "17/20",
    "breakdown": {{
        "CategoryName": {{
        "score": string, // formatted exactly like "17/20",
        "feedback": string
        }}
    }},
    "suggested_fixes": ["fix 1", "fix 2"]
    }}
    """

    return prompt


def grade_assignment(assignment_text, rubric_text):
    prompt = build_prompt(assignment_text, rubric_text)

    response = client.responses.create(
        input=prompt,
        model="llama-3.1-8b-instant",
        temperature=0
    )

    return response.output_text
