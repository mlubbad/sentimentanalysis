import requests
import pandas as pd

# API Constants
LAMA3_API_KEY = "xxxxxxxxxxxxxxxx"
LAMA3_BASE_URL = "https://api.perplexity.ai/chat/completions"

# Load data (replace with actual data source, e.g., a CSV file or database)
def load_data(file_path):
    return pd.read_csv(file_path)

# Save data (for updating processed results)
def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# Function to reset last processed index
def reset_last_processed_index():
    try:
        return 0
    except Exception as e:
        print(f"Error resetting last processed index: {e}")
        return None

# Function to check if a batch processing trigger is set
def is_trigger_set():
    # For Python scripts, you would manage triggers using scheduled tasks (e.g., cron jobs) or similar.
    return False  # Placeholder for actual implementation

# Function to extract text from API response
def extract_text(json_response):
    if not json_response or "content" not in json_response:
        print("Invalid JSON response structure")
        return ""
    return " ".join(
        item["text"]
        for item in json_response["content"]
        if item.get("type") == "text"
    )

# Function to process search terms and get sentiment analysis
def sentiment_analyse(data, start_index=0, batch_size=100):
    end_index = min(start_index + batch_size, len(data))
    for i in range(start_index, end_index):
        search_term = data.loc[i, "SearchTerm"]
        existing_question = data.loc[i, "Sentiment"]

        # Skip if already processed
        if pd.notna(existing_question):
            continue

        messages = [
            {"role": "user", "content": f"Comment: '{search_term}'"},
        ]
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {LAMA3_API_KEY}",
        }
        payload = {
            "model": "llama-3.1-sonar-large-128k-chat",
            "messages": messages,
            "temperature": 0,
        }

        try:
            response = requests.post(LAMA3_BASE_URL, headers=headers, json=payload)
            response_data = response.json()
            sentiment_result = extract_text(response_data)
            if sentiment_result:
                data.loc[i, "Sentiment"] = sentiment_result
                print(f"Processed {i + 1}/{len(data)}: {sentiment_result}")
        except Exception as e:
            print(f"Error processing term '{search_term}': {e}")

    return data

# Main execution
if __name__ == "__main__":
    # File path to the dataset
    file_path = "search_terms.csv"

    # Load the data
    data = load_data(file_path)

    # Reset or get the last processed index
    last_processed_index = reset_last_processed_index()

    # Process sentiment analysis
    updated_data = sentiment_analyse(data, start_index=last_processed_index)

    # Save updated data
    save_data(updated_data, file_path)
