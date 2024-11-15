import re
from PyPDF2 import PdfReader
from fpdf import FPDF

# Function to extract only questions and their options
def extract_questions(pdf_path):
    reader = PdfReader(pdf_path)
    questions = []
    question_pattern = re.compile(r'(\d+\.\s+.*?)((?:[a-d]\.\s+.*?)+)', re.DOTALL)

    for page in reader.pages:
        page_text = page.extract_text()
        matches = question_pattern.findall(page_text)

        for match in matches:
            question_text = match[0].strip()
            options_text = match[1].strip()

            # Split options by pattern like "A. ", "B. ", etc.
            options = re.findall(r'[a-d]\.\s+.*?(?=(?:\s[a-d]\.\s|$))', options_text, re.DOTALL)
            
            if len(options) == 4:  # Ensure we have exactly four options
                questions.append((question_text, options))
    
    return questions

# Function to write extracted questions and options to a PDF
def write_to_pdf(questions, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for i, (question, options) in enumerate(questions, start=1):
        pdf.cell(0, 10, f"{i}. {question}", ln=True)
        for option in options:
            pdf.cell(0, 10, option, ln=True)
        pdf.cell(0, 10, "", ln=True)  # Add a line break between questions
    
    pdf.output(output_pdf)

# Path to input PDF and output PDF
input_pdf = "input.pdf"
output_pdf = "outputrr.pdf"

# Extract questions and write to PDF
questions = extract_questions(input_pdf)
write_to_pdf(questions, output_pdf)

