import tkinter as tk
from tkinter import ttk
import gspread
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

# Create a function to perform the Google Sheets and OpenAI operations
def perform_operations():
    # Get user input from the entry widget
    user_input = entry.get()

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

            # # Convert 'Value' to numeric, replacing non-numeric values with NaN
            # df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

            # # Replace NaN values in 'Value' with 0
            # df['Value'].fillna(0, inplace=True)

            # Ask a question
            answer = df.chat(user_input)

            # Print the answer
            print("Answer:", answer)

            # Display the answer in the result_label
            result_label.config(text=answer)

        except gspread.exceptions.APIError as e:
            print(f"Google Sheets API error: {e}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(f"Unable to open the Google Sheet: {sheet_title}")

    except Exception as e:
        # Handle errors here and display an error message
        result_label.config(text=f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Google Sheets and OpenAI Integration")

# Create and place an entry widget for user input
entry = ttk.Entry(root, width=50)
entry.pack(pady=10)

# Create and place a button to trigger the operations
button = ttk.Button(root, text="Ask Question", command=perform_operations)
button.pack()

# Create and place a label to display the answer
result_label = ttk.Label(root, text="", wraplength=400)
result_label.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
