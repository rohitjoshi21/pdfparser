def format_to_markdown(input_file, output_file):
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split into individual questions
        questions = content.split('\nQuestion ')[1:]  # Skip the first empty split
        
        formatted_questions = []
        for question in questions:
            lines = question.strip().split('\n')
            
            # Get question number from first line
            question_num = lines[0].split(':')[0]
            
            # Start building formatted question
            formatted_question = []
            
            # Add question header with bold formatting
            current_question_text = []
            
            in_options = False
            for line in lines[1:]:  # Skip the "Question X:" line
                # Check if this is an option line (starts with a., b., c., or d.)
                if line.strip().startswith(('a.', 'b.', 'c.', 'd.')):
                    # If we were building a question text, add it now
                    if current_question_text:
                        formatted_question.append(f"**Q{' '.join(current_question_text)}**\n")
                        current_question_text = []
                    # Add indented option
                    formatted_question.append(f"    {line.strip()}")
                    in_options = True
                else:
                    if not in_options:
                        # Still part of question text
                        current_question_text.append(line.strip())
                    else:
                        # Must be a new question starting
                        in_options = False
                        current_question_text = [line.strip()]
            
            # Add any remaining question text
            if current_question_text:
                formatted_question.append(f"**Q{question_num}. {' '.join(current_question_text)}**")
            
            # Add formatted question to list with proper spacing
            formatted_questions.append('\n'.join(formatted_question))
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('# Medical Entrance Examination Questions\n\n')
            file.write('\n\n'.join(formatted_questions))
            
        print(f"Successfully formatted questions to {output_file}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def main():
    input_file = 'questions_output.txt'  # The output from previous script
    output_file = 'formatted_questions.md'  # New markdown file
    format_to_markdown(input_file, output_file)

if __name__ == "__main__":
    main()