import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Constants for API and OAuth
API_KEY = "xxxxxxxxxxxxxxxxxxxx"  # Replace with your actual API key
TOKEN = "xxxxxxxxx..."  # Replace with your actual token
MODEL = "models/gemini-1.5-pro-002"
BASE_URL = f"https://us-central1-aiplatform.googleapis.com/v1/projects/gen-lang-client-0861677080/locations/us-central1/publishers/google/models/{MODEL}:generateContent"
BATCH_SIZE = 1000

# Authenticate with Google Sheets
def authenticate_google_sheets(credentials_file):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

# Load data from Google Sheets
def load_sheet_data(sheet):
    records = sheet.get_all_records()
    return pd.DataFrame(records)

# Save data back to Google Sheets
def save_sheet_data(sheet, data):
    for i, row in data.iterrows():
        sheet.update_cell(i + 2, 2, row['Sentiment'])  # Update column B with sentiment analysis

# API call to process search terms
def call_api(search_term, video_url=None):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }
    body = {
        "contents": [
            {"role": "user", "parts": [{"text": f"Comment: {search_term}"}]}
        ],
        "generationConfig": {
            "maxOutputTokens": 8192,
            "temperature": 0,
            "topP": 0.95,
        }
    }
    if video_url:
        body["contents"].append({"role": "user", "parts": [{"text": f"Video URL: {video_url}"}]})
    response = requests.post(BASE_URL, headers=headers, json=body)
    if response.status_code == 200:
        response_data = response.json()
        candidates = response_data.get("candidates", [])
        if candidates:
            return candidates[0]["content"]["parts"][0]["text"].strip()
    else:
        print(f"API Error: {response.status_code} - {response.text}")
    return None

# Process a batch of search terms
def process_batch(data, start_index, batch_size):
    end_index = min(start_index + batch_size, len(data))
    for i in range(start_index, end_index):
        search_term = data.loc[i, "SearchTerm"]
        video_url = data.loc[i, "VideoURL"] if "VideoURL" in data.columns else None
        if pd.isna(data.loc[i, "Sentiment"]):  # Only process if sentiment is not already set
            sentiment = call_api(search_term, video_url)
            data.loc[i, "Sentiment"] = sentiment
            print(f"Processed {i + 1}/{len(data)}: {sentiment}")
    return data

# Main execution function
def main():
    # Google Sheets authentication
    credentials_file = "path/to/credentials.json"  # Replace with your Google Sheets API credentials file
    client = authenticate_google_sheets(credentials_file)
    
    # Open the spreadsheet and select the sheet
    spreadsheet = client.open("Sentiment Analysis")
    sheet = spreadsheet.sheet1  # Replace with the actual sheet name if necessary

    # Load data
    data = load_sheet_data(sheet)

    # Process batches
    last_processed_index = 0  # Replace with logic to store/retrieve the last processed index
    updated_data = process_batch(data, last_processed_index, BATCH_SIZE)

    # Save updated data
    save_sheet_data(sheet, updated_data)

if __name__ == "__main__":
    main()
