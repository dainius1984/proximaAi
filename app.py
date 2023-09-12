from flask import Flask, render_template, request
import gspread
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

app = Flask(__name__)

def perform_operations(user_input):
    try:
        gc = gspread.service_account(filename="/Users/marcinchmielnicki/panda/Proximagoogle.json")
        sheet_title = "THE FS TAM"
        
        sheet = gc.open(sheet_title)
        worksheet = sheet.get_worksheet(0)
        values = worksheet.get_all_values()

        df = pd.DataFrame(values[1:], columns=values[0])
        df = SmartDataframe(df, config={"llm": OpenAI(api_token="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")})
        
        answer = df.chat(user_input)
        print("Type of answer:", type(answer))
        print("Content of answer:", answer)
        
        answer_list = []

        if isinstance(answer, SmartDataframe):
            answer_list = answer['Company'].tolist()
        elif isinstance(answer, str):
            answer_list = [item.strip() for item in answer.split(',')]
        else:
            answer_list = [answer]

        return answer_list

    except gspread.exceptions.APIError as e:
        print(f"Google Sheets API error: {e}")
        return [f"Google Sheets API error: {e}"]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return [f"An error occurred: {str(e)}"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        user_input = request.form['user_input']
        answer_list = perform_operations(user_input)
        return render_template('result.html', answer_list=answer_list)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
