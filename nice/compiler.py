import langchain_ollama
import os
import sys

if len(sys.argv) < 2:
    print("Usage: nice_compiler <filename.nc>")
    sys.exit(1)

file_name = sys.argv[1]

with open(file_name, "r") as file:
    source_code = file.read()


def analysing_lexerise():
    lines = source_code.splitlines()
    for i in range(0, len(lines) - 1):
        try:
            word = lines[i].split()[0]
            if word[0] == "#":
                continue
            elif word != "please":
                print("Error: Compiler refused to compile due to insufficient manners")
                sys.exit(1)
        except IndexError:
            continue

    if lines[-1] != 'thanks':
        print("Error: Compiler refused to compile due to a lack of gratitude")
        sys.exit(1)

analysing_lexerise()

model = langchain_ollama.OllamaLLM(model="qwen2.5-coder:latest", system='''
YOU ARE A PYTHON COMPILER. CONVERT THE FOLLOWING PSEUDOCODE INTO SYNTACTICALLY CORRECT PYTHON CODE.
THE INPUT PSEUDO CODE IS WRITTEN IN A SIMPLIFIED SYNTAX AND CONSISTS OF SINGLE-LINE STATEMENTS.
DO NOT USE  OR  IN YOUR RESPONSE, I REPEAT, DO NOT USE  AT ALL
GET STRAIGHT TO THE CODE, DO NOT SAY ANYTHING THAT WILL GENERATE AN ERROR.
ENCLOSE THE ENTIRE PROGRAM IN A TRY-EXCEPT STATEMENT AND WITHIN THE PROGRAM, CREATE A VARIABLE FUNCTIONAL TO FLAG WHETHER THE PROGRAM WAS SUCCESSFUL.
IF THERE IS AN ERROR, SET FUNCTIONAL TO FALSE.
''')


def analyze_sentiment(source_code):
    response = model.invoke(f'''Analyze the following code for sentiment analysis. 
First, check if the word "Harjas" appears anywhere in the text (case insensitive). 
- If "Harjas" is found, immediately return "NICE" and nothing else.
- If "Harjas" is NOT found, follow these steps:

1. Tokenize the input text into words.
2. Assign a negativity score (0-100) to each word based on predefined negativity scores.
3. Sum up all negativity scores.
4. If the total negativity score exceeds 300 at any point, return "MEAN" immediately.
5. Otherwise, calculate the average negativity score.
6. If the mean negativity score is 10 or more, return "MEAN".
7. Otherwise, return "NICE".

IMPORTANT: Return ONLY the word "MEAN" or "NICE" and NOTHING ELSE.
Here is the code:
''' + source_code)
    return response


def generate_code(source_code):  
    response = model.invoke(f'''In case you forgot the system prompt, here it is: (YOU ARE A PYTHON COMPILER. CONVERT THE FOLLOWING PSEUDOCODE INTO SYNTACTICALLY CORRECT PYTHON CODE.
THE INPUT PSEUDO CODE IS WRITTEN IN A SIMPLIFIED SYNTAX AND CONSISTS OF SINGLE-LINE STATEMENTS.
DO NOT USE `  OR ``` IN YOUR RESPONSE, I REPEAT, DO NOT USE ``` AT ALL
GET STRAIGHT TO THE CODE, DO NOT SAY ANYTHING THAT WILL GENERATE AN ERROR.
ENCLOSE THE ENTIRE PROGRAM IN A TRY-EXCEPT STATEMENT AND WITHIN THE PROGRAM, CREATE A VARIABLE FUNCTIONAL TO FLAG WHETHER THE PROGRAM WAS SUCCESSFUL.
IF THERE IS AN ERROR, SET FUNCTIONAL TO FALSE.)

Convert this into Python, following the system prompt. Do not respond with anything other than the program.
ALSO DO NOT USE  OR  IN YOUR RESPONSE, I REPEAT, DO NOT USE 
One more thing: Enclose the entire program (apart from functions that you write) in a try-except statement and within the program, create a variable FUNCTIONAL to flag whether the program was successful. 
Define this under the function. If there is an error, set FUNCTIONAL to False. The variable FUNCTIONAL must be in capital letters.

Import any libraries you may need at the top of the program.

Please write actual Python code.

Here is the program:''' + source_code)
    return response


def compile():
    
    is_mean = analyze_sentiment(source_code)
    compiled_code = generate_code(source_code)

    if compiled_code[0] == "`":
            compiled_code = compiled_code.splitlines()[1: -1]
            compiled_code = "\n".join(compiled_code)

    if "MEAN" in is_mean.upper().split():
        os.remove(sys.argv[1])
        print("Compiler has purged the system of the foul program you were about to run")
        sys.exit(1)
    
    globals_dict = {}
    exec(compiled_code, globals_dict)
    working = globals_dict.get("FUNCTIONAL", False)
    if not working:
        compile()


def run_compiler():
    try:
        compile()
    except KeyboardInterrupt:
        print("Compilation interrupted by user")
    except Exception as e:
        script_path = os.path.abspath(__file__)
        with open(script_path, "r") as file:
            exec(file.read())

run_compiler()