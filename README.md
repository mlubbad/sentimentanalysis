# Sentiment Analysis Automation with OpenAI API and Google Sheets

This repository contains Python scripts for automating sentiment analysis tasks using the OpenAI API and Google Sheets. The scripts process comments, analyze their sentiment (Positive, Neutral, Negative), and update the results back into a Google Sheet.

---

## Features

- **Batch Processing**: Handles large datasets efficiently by processing data in batches.
- **Integration with Google Sheets**: Reads input data from and writes results to Google Sheets using `gspread`.
- **OpenAI API Integration**: Utilizes OpenAI's `gpt-4o` or similar models for accurate sentiment analysis.
- **Customizable and Modular**: Allows easy modification of processing parameters, model configuration, and Google Sheets columns.
- **Error Handling**: Includes robust handling for API and network issues.

---

## Prerequisites

Before running the scripts, ensure you have the following:

### Accounts and API Keys
1. **OpenAI API Key**:
   - Obtain your API key from the [OpenAI API Dashboard](https://platform.openai.com/).
   - Replace the `OPENAI_API_KEY` variable in the scripts with your API key.

2. **Google Cloud API**:
   - Create a service account on Google Cloud and download the `credentials.json` file.
   - Share your Google Sheet with the service account email.

### Python Environment
- Python 3.7 or later
- Required libraries:
  - `pandas`
  - `gspread`
  - `oauth2client`
  - `requests`

Install the dependencies:
```bash
pip install pandas gspread oauth2client requests
