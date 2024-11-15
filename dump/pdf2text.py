import PyPDF2
from fpdf import FPDF
import re

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() or ""
    return text

def sanitize_text(text):
    # Replace unsupported characters with ASCII equivalents or remove them
    replacements = {
        '\u2022': '-',  # Bullet to dash
        '\u2013': '-',  # En dash to dash
        '\u2014': '-',  # Em dash to dash
        '\u201c': '"',  # Left double quote to "
        '\u201d': '"',  # Right double quote to "
        '\u2018': "'",  # Left single quote to '
        '\u2019': "'",  # Right single quote to '
        '\uf0b7': '-',  # Alternate bullet to dash
    }
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    
    # Remove any remaining non-ASCII characters
    return text.encode('ascii', 'ignore').decode('ascii')

def extract_questions(text):
    question_pattern = r"\n(\d{1,3}\. .+?)\n(a.+?)\n(b.+?)\n(c.+?)\n(d.+?)Ans:"

    questions = re.findall(question_pattern, text, re.DOTALL)
    return [sanitize_text(q[0].strip()) for q in questions]

def write_to_pdf(questions, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    print(questions[0])
    for question in questions:
        pdf.multi_cell(0, 10, question)
        pdf.ln()
    
    pdf.output(output_pdf)

# Usage
pdf_path = 'input.pdf'
output_pdf = 'output_questions.pdf'

# Extract and process text
text = pdf_to_text(pdf_path)
questions = extract_questions(text)
write_to_pdf(questions, output_pdf)

