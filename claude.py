import re

def clean_text(text):
    # Remove asterisks and extra whitespace
    cleaned = re.sub(r'\*+', '', text)
    cleaned = ' '.join(cleaned.split())
    return cleaned

def extract_questions(content):
    # Split content into lines
    lines = content.split('\n')
    
    questions = []
    current_question = []
    in_question = False
    skip_next = False
    
    for i, line in enumerate(lines):
        clean_line = clean_text(line)
        
        # Skip empty lines and headers
        if not clean_line or clean_line.startswith('#') or clean_line.startswith('-----'):
            continue
            
        # Detect start of question - look for numbered patterns
        if (re.match(r'^\d+\.', clean_line) or 
            re.search(r'\d+\.\s+[A-Z]', clean_line) or
            re.search(r'^\d+\.\s+[A-Z]', clean_line)):
            
            # Save previous question if exists
            if current_question:
                questions.append('\n'.join(current_question))
                current_question = []
            
            in_question = True
            current_question.append(clean_line)
            continue
        
        # Detect options
        if re.match(r'^[abcd]\.\s', clean_line):
            if in_question:
                current_question.append(clean_line)
            continue
        
        # If we find an answer, save the current question and move to next
        if clean_line.startswith('Ans:'):
            in_question = False
            if current_question:
                questions.append('\n'.join(current_question))
                current_question = []
            continue
            
        # If we're in a question and the line isn't metadata, add it
        if in_question and not any(clean_line.startswith(x) for x in ['Ref:', 'Author:', '-']):
            if clean_line:
                current_question.append(clean_line)
    
    # Add the last question if exists
    if current_question:
        questions.append('\n'.join(current_question))
    
    return questions

def main():
    try:
        # Read the file - print first few lines for debugging
        with open('output.md', 'r', encoding='utf-8') as file:
            content = file.read()
            print("First 200 characters of input file:")
            print(content[:200])
            print("---")
        
        # Extract questions
        questions = extract_questions(content)
        
        # Print number of questions found
        print(f"Found {len(questions)} questions")
        
        # Write to output file
        with open('questions_output.txt', 'w', encoding='utf-8') as file:
            for i, question in enumerate(questions, 1):
                file.write(f"Question {i}:\n{question}\n\n")
        
        # Print first question for verification
        if questions:
            print("\nFirst question extracted:")
            print(questions[0])
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()