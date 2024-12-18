import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Constants
OPENAI_API_KEY = 'sk-xxxxx..'
BASE_URL = "https://api.openai.com/v1/chat/completions"
BATCH_SIZE = 50

# Authenticate with Google Sheets
def authenticate_google_sheets(credentials_file):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

# Load data from Google Sheets
def load_data(sheet):
    records = sheet.get_all_records()
    return pd.DataFrame(records)

# Save data to Google Sheets
def save_data(sheet, data):
    for i, row in data.iterrows():
        sheet.update_cell(i + 2, 2, row['Sentiment'])  # Assuming sentiment results are in column B

# Reset the last processed index
def reset_last_processed_index():
    return 0

# Call OpenAI API
def call_openai_api(messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    payload = {
        "model": "gpt-4o",  # Replace with your model
        "messages": messages,
    }
    try:
        response = requests.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        if "choices" in response_data:
            return response_data["choices"][0]["message"]["content"].strip()
        else:
            print("Invalid response structure:", response_data)
            return None
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return None

# Process batch of rows
def process_batch(data, start_index):
    end_index = min(start_index + BATCH_SIZE, len(data))
    for i in range(start_index, end_index):
        search_term = data.loc[i, "SearchTerm"]
        if pd.isna(data.loc[i, "Sentiment"]):  # Only process if sentiment is not already set
            messages = [
                {
                    "role": "system",
                    "content": "You are a data analyst tasked with analyzing comments on a comedic political show. Provide a sentiment analysis (Positive, Neutral, or Negative).",
                },
                {"role": "user", "content": search_term},
            ]
            sentiment = call_openai_api(messages)
            data.loc[i, "Sentiment"] = sentiment
            print(f"Processed row {i}: {sentiment}")
    return data

# Main function
def main():
    # Authenticate Google Sheets
    credentials_file = "path/to/your/credentials.json"  # Replace with the actual path
    client = authenticate_google_sheets(credentials_file)

    # Open the spreadsheet and sheet
    spreadsheet = client.open("Sentiment Analysis")  # Replace with your spreadsheet name
    sheet = spreadsheet.sheet1  # Replace with your sheet name if necessary

    # Load data
    data = load_data(sheet)

    # Reset or get the last processed index
    last_processed_index = reset_last_processed_index()

    # Process data in batches
    updated_data = process_batch(data, last_processed_index)

    # Save updated data
    save_data(sheet, updated_data)

if __name__ == "__main__":
    main()
