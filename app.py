from flask import Flask, render_template, request
import gspread
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

app = Flask(__name__)

def perform_operations(user_input):
    try:
        gc = gspread.service_account(filename="/Users/marcinchmielnicki/panda/Proximagoogle.json")

        sheet_titles = [
            # "THE FS TAM"  # Replace with the title of your first Google Sheet
            "LS TECH"     # Add the title of your second Google Sheet
        ]

        answer_list = []

        for sheet_title in sheet_titles:
            sheet = gc.open(sheet_title)
            worksheet = sheet.get_worksheet(0)
            values = worksheet.get_all_values()

            df = pd.DataFrame(values[1:], columns=values[0])
            
            custom_sample_data = {
                'Industry': ['Financial Services', 'Life Sciences'],  # Provide your own examples here
                'Market Segment': ['Capital Market', 'CIB', 'Wealth Mgmt'],        # Provide your own examples here
                'Market Sub-Segment': ['Investment Bank', 'Front Office', 'Digital Assets'],  # Provide your own examples here
                'Product Category': ['Remittance Services', 'Lending'],  # Provide your own examples here
            }

            # Create a custom description
            description = "This SmartDataFrame contains data with custom sample data for each column."

            # Instantiate a SmartDataframe with a custom description
            df = SmartDataframe(df, config={"llm": OpenAI(api_token="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")},
                                 description=description)

            # Add custom sample data as an attribute of the SmartDataframe
            df.custom_sample_data = custom_sample_data

            answer = df.chat(user_input)
            print("Type of answer:", type(answer))
            print("Content of answer:", answer)

            if isinstance(answer, SmartDataframe):
                answer_list.extend(answer['Company'].tolist())
            elif isinstance(answer, str):
                answer_list.extend(item.strip() for item in answer.split(','))
            else:
                answer_list.append(answer)

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