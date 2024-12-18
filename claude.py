import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Constants
ANTHROPIC_API_KEY = "xxxxxxxxxxxxx...."
API_URL = "https://api.anthropic.com/v1/messages"
BATCH_SIZE = 45

# Authenticate Google Sheets
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
        sheet.update_cell(i + 2, 2, row['Sentiment'])  # Assuming 'Sentiment' is written in column B

# Extract text from the API response
def extract_text(response_json):
    if not response_json or "content" not in response_json:
        print("Invalid JSON response structure")
        return None
    return response_json.get("content", "")

# Make API request
def call_api(messages):
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1024,
        "messages": messages,
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        return extract_text(response_data)
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return None

# Process a batch of rows
def process_batch(data, start_index):
    end_index = min(start_index + BATCH_SIZE, len(data))
    for i in range(start_index, end_index):
        search_term = data.loc[i, "SearchTerm"]
        if pd.isna(data.loc[i, "Sentiment"]):  # Only process rows without Sentiment
            messages = [
                {
                    "role": "user",
                    "content": f"You are a data analyst and data scientist assigned to analyze comments on a show. Analyze the sentiment of: {search_term}",
                }
            ]
            sentiment = call_api(messages)
            data.loc[i, "Sentiment"] = sentiment
            print(f"Processed row {i}: {sentiment}")
    return data

# Main function
def main():
    # Authenticate Google Sheets
    credentials_file = "path/to/your/credentials.json"  # Replace with your credentials file
    client = authenticate_google_sheets(credentials_file)

    # Open the spreadsheet
    spreadsheet = client.open("Sentiment Analysis")  # Replace with your spreadsheet name
    sheet = spreadsheet.sheet1  # Replace with your sheet name if necessary

    # Load data
    data = load_data(sheet)

    # Process data in batches
    start_index = 0  # Adjust based on your requirement
    updated_data = process_batch(data, start_index)

    # Save updated data
    save_data(sheet, updated_data)

if __name__ == "__main__":
    main()
