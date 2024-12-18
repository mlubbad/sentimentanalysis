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
```

## Setup

### Clone the repository:

```bash
git clone https://github.com/yourusername/sentiment-analysis-automation.git
cd sentiment-analysis-automation
```
Place the credentials.json file in the root of the repository.

### Update the following variables in the scripts:

- OpenAI API Key: Replace the OPENAI_API_KEY constant with your actual key.
- Google Sheet Name: Replace "Sentiment Analysis" with the name of your Google Sheet.
### Ensure the Google Sheet has the following structure:

- Column A: SearchTerm (input text)
- Column B: Sentiment (blank, to store analysis results)
### Usage
Run the script to process data and update the Google Sheet:

```bash
python script_name.py
```

### Key Parameters
- BATCH_SIZE: Set the number of rows to process in a single batch (default: 50).
- model: Adjust the OpenAI model being used (e.g., gpt-4o, gpt-3.5-turbo).

### Example Workflow

### Input:

Add comments or text data to column SearchTerm in the Google Sheet.

### Processing:
- The script reads the data, sends it to the OpenAI API for sentiment analysis, and updates the results.

### Output:
- The Sentiment column in the Google Sheet is updated with the analysis results.

### Error Handling
- API Failures: If the API request fails, the error is logged, and the script continues processing the next batch.
- Sheet Access Issues: Ensure the Google Sheet is shared with the service account email if access errors occur.
Customization

### Column Names:
- Update the column names in the script (SearchTerm, Sentiment) if your sheet uses different headers.
Data Processing:
- Modify the call_openai_api() function to use custom messages or parameters.

### Batch Size:
- Change the BATCH_SIZE constant for processing larger or smaller data chunks.

### Limitations
- Rate Limits: Adhere to OpenAI's API rate limits to avoid throttling.
- Data Privacy: Ensure sensitive data is handled securely when using third-party APIs.

### License
This project is licensed under the MIT License.

### Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for improvements or bug fixes.

### Contact
For questions or support, contact yourname@domain.com.


