from flask import Flask, render_template, request
import gspread
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

app = Flask(__name__)

def perform_operations(user_input):
    try:
        # Authenticate with Google Sheets using the JSON key file
        gc = gspread.service_account(filename="/Users/marcinchmielnicki/panda/Proximagoogle.json")
        sheet_title = "THE FS TAM"
        
        # Open the Google Sheet by title
        sheet = gc.open(sheet_title)
        worksheet = sheet.get_worksheet(0)
        values = worksheet.get_all_values()

        # Create a DataFrame from the values
        df = pd.DataFrame(values[1:], columns=values[0])
        df = SmartDataframe(df, config={"llm": OpenAI(api_token="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")})
        
        # Ask a question
        answer = df.chat(user_input)
        print("Type of answer:", type(answer))
        print("Content of answer:", answer)
            
        if isinstance(answer, SmartDataframe):
            answer = answer.to_dataframe()  # This is the hypothesized change
        
        # Other parts of the code
        ...

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        user_input = request.form['user_input']
        answer = perform_operations(user_input)

        # Render the result
        ...

    return render_template('index.html', result=None)

if __name
