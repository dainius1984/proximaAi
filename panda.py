from flask import Flask, render_template, request

import gspread
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

app = Flask(__name__)

# Create a function to perform the Google Sheets and OpenAI operations
def perform_operations(user_input):
    try:
        # Authenticate with Google Sheets using the JSON key file
        gc = gspread.service_account(filename="/Users/marcinchmielnicki/panda/Proximagoogle.json")

        # Specify the Google Sheet title you want to open
        sheet_title = "THE FS TAM"  # Replace with your actual sheet title

        try:
            # Open the Google Sheet by title
            sheet = gc.open(sheet_title)
            print(f"Successfully opened the Google Sheet: {sheet_title}")

            # Select a specific worksheet by title (or use get_worksheet() to select by index)
            worksheet = sheet.get_worksheet(0)  # Assuming you want to work with the first worksheet (index 0)

            # Get all values from the worksheet
            values = worksheet.get_all_values()
            print("Google Sheet Data:")
            print(values)

            # Create a DataFrame from the values
            df = pd.DataFrame(values[1:], columns=values[0])  # Assuming the first row contains column names

            # Create a SmartDataFrame
            df = SmartDataframe(df, config={"llm": OpenAI(api_token="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")})  # Replace with your OpenAI API token

            # Ask a question
            answer = df.chat(user_input)

            # Print the answer
            print("Answer:", answer)

            return answer

        except gspread.exceptions.APIError as e:
            print(f"Google Sheets API error: {e}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(f"Unable to open the Google Sheet: {sheet_title}")

    except Exception as e:
        # Handle errors here and return an error message
        return f"An error occurred: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        result = perform_operations(user_input)
        return render_template('index.html', result=result)
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
