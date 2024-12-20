import google.generativeai as genai
import ast
import json
from PIL import Image
from .constants import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def analyze_image(img: Image, dict_of_vars: dict):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    dict_of_vars_str = json.dumps(dict_of_vars, ensure_ascii=False)
    prompt = (
        f"You have been given an image with some mathematical expressions, equations, or graphical problems, and you need to solve them. "
        f"Note: Use the PEMDAS rule for solving mathematical expressions. PEMDAS stands for the Priority Order: Parentheses, Exponents, Multiplication and Division (from left to right), Addition and Subtraction (from left to right). Parentheses have the highest priority, followed by Exponents, then Multiplication and Division, and lastly Addition and Subtraction. "
        f"For example: "
        f"Q. 2 + 3 * 4 "
        f"(3 * 4) => 12, 2 + 12 = 14. "
        f"Q. 2 + 3 + 5 * 4 - 8 / 2 "
        f"5 * 4 => 20, 8 / 2 => 4, 2 + 3 => 5, 5 + 20 => 25, 25 - 4 => 21. "
        f"YOU CAN HAVE FIVE TYPES OF EQUATIONS/EXPRESSIONS IN THIS IMAGE, AND ONLY ONE CASE SHALL APPLY EVERY TIME: "
        f"Following are the cases: "
        f"1. Simple mathematical expressions like 2 + 2, 3 * 4, 5 / 6, 7 - 8, etc.: In this case, solve and return the answer in the format: [{{'expr': '2 + 2', 'result': '4'}}]. "
        f"2. Set of Equations like x^2 + 2x + 1 = 0, 3y + 4x = 0, 5x^2 + 6y + 7 = 12, etc.: In this case, solve for the given variable, and the format should be: [{{'expr': 'x', 'result': '2', 'assign': True}}, {{'expr': 'y', 'result': '5', 'assign': True}}]. "
        f"3. Assigning values to variables like x = 4, y = 5, z = 6, etc.: In this case, return: [{{'expr': 'x', 'result': '4', 'assign': True}}]. "
        f"4. Graphical Math problems: Return [{{'expr': 'problem description', 'result': 'numerical answer'}}]. "
        f"5. Abstract Concepts: Return [{{'expr': 'drawing explanation', 'result': 'concept name'}}]. "
        f"IMPORTANT: "
        f"- ALL text values must be strings (wrapped in quotes) "
        f"- Format must be a valid Python list of dictionaries "
        f"- Use single quotes for strings "
        f"- For mathematical expressions, return the result as a string "
        f"Here is a dictionary of user-assigned variables to use if needed: {dict_of_vars_str}"
    )
    
    try:
        response = model.generate_content([prompt, img])
        print("Raw Gemini response:", response.text)
        
        # Try to clean and format the response if needed
        text = response.text.strip()
        if not text.startswith('['):
            # If response isn't a list, try to extract list from the text
            import re
            list_match = re.search(r'\[(.*?)\]', text, re.DOTALL)
            if list_match:
                text = list_match.group(0)
            else:
                # If no list found, try to create one from the response
                text = f"[{{'expr': '{text}', 'result': ''}}]"
        
        try:
            answers = ast.literal_eval(text)
        except (SyntaxError, ValueError) as e:
            print(f"First parsing attempt failed: {e}")
            # Try cleaning the text more aggressively
            text = text.replace('"', "'")  # Replace double quotes with single quotes
            text = re.sub(r"'result':\s*([^',}\]]+)[,}\]]", r"'result': '\1'\1", text)  # Ensure result is quoted
            try:
                answers = ast.literal_eval(text)
            except (SyntaxError, ValueError) as e:
                print(f"Second parsing attempt failed: {e}")
                # Return a formatted error response
                answers = [{
                    'expr': text[:100] + '...' if len(text) > 100 else text,
                    'result': f'Error parsing response: {str(e)}',
                    'error': True
                }]
    except Exception as e:
        print(f"Error in Gemini API call: {e}")
        answers = [{
            'expr': 'API Error',
            'result': str(e),
            'error': True
        }]

    # Ensure assign field is present in all answers
    for answer in answers:
        if 'assign' not in answer:
            answer['assign'] = False
        if not isinstance(answer['expr'], str):
            answer['expr'] = str(answer['expr'])
        if not isinstance(answer['result'], str):
            answer['result'] = str(answer['result'])
    
    print('Returned answer:', answers)
    return answers
