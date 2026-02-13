import pdfplumber


def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            # checking to make sure text is not None
            if page.extract_text():
                text = text + page.extract_text()
    return text


def extract_rubric(pdf_file):
    rubric_table = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    for row in table:
                        # remove empty cells and strip whitespace
                        cleaned_row = [cell.strip() for cell in row if cell]
                        if cleaned_row:  # skip empty rows
                            rubric_table.append(cleaned_row)

    if rubric_table:
        return rubric_table
    else:
        return extract_text(pdf_file)
