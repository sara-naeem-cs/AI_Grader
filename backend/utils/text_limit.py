
MAX_CHARS_ASSIGNMENT = 6000
MAX_CHARS_RUBRIC = 3000


def size_limit_assignment(assignment_text):
    if assignment_text:
        assignment_text = assignment_text[:MAX_CHARS_ASSIGNMENT]
    else:
        assignment_text = ""
    return assignment_text


def size_limit_rubric(rubric_text):
    if not rubric_text:
        return [] if isinstance(rubric_text, list) else ""

    # If it's a string, just slice
    if isinstance(rubric_text, str):
        return rubric_text[:MAX_CHARS_RUBRIC]

    # If it's a table, go through array of arrays
    limited_table = []
    chars_used = 0

    for row in rubric_text:
        limited_row = []
        for cell in row:
            remaining = MAX_CHARS_RUBRIC - chars_used
            if remaining <= 0:
                break
            # Truncate cell if it would exceed the limit
            truncated_cell = cell[:remaining] if len(
                cell) > remaining else cell
            limited_row.append(truncated_cell)
            chars_used += len(truncated_cell)
        if limited_row:
            limited_table.append(limited_row)
        if chars_used >= MAX_CHARS_RUBRIC:
            break

    return limited_table
