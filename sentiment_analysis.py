# ======================
# INSTALL REQUIRED PACKAGES
# ======================
!pip install --upgrade gspread transformers pandas torch torchaudio --no-cache-dir

# ======================
# AUTHENTICATE WITH GOOGLE (Colab only)
# ======================
from google.colab import auth
auth.authenticate_user()

import gspread
from google.auth import default
import pandas as pd
from transformers import pipeline
import torch

# ======================
# SENTIMENT CONFIGURATION
# ======================
SENTIMENT_LABELS = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive",
}

# Initialize RoBERTa model for sentiment
sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

# ======================
# ANALYSIS FUNCTION
# ======================
def analyze_text(text):
    """Run sentiment analysis using RoBERTa"""
    result = sentiment_model(text)[0]
    sentiment_label = SENTIMENT_LABELS.get(result["label"], result["label"])
    sentiment_score = round(result["score"], 3)

    return {
        "text": text,
        "sentiment": sentiment_label,
        "sentiment_score": sentiment_score
    }

# ======================
# SAMPLE ARTICLE DATA
# ======================
article = {
    "title": "US aid cuts strain response to health crises worldwide: WHO",
    "narratives": [
        "The United States slashing foreign aid risks piling pressure on already acute humanitarian crises...",
        "Washington did not pay its 2024 dues, and it remains unclear if it will meet obligations for 2025...",
        "The funding cuts will likely hinder aid to communities in desperate need of care.",
    ],
}

# ======================
# PROCESS CONTENT
# ======================
results = []

# Analyze title
title_analysis = analyze_text(article["title"])
title_analysis["text_type"] = "Title"
results.append(title_analysis)

# Analyze narratives
for idx, text in enumerate(article["narratives"]):
    if text:
        analysis = analyze_text(text)
        analysis["text_type"] = f"Narrative {idx+1}"
        results.append(analysis)

# Create DataFrame
df = pd.DataFrame(results)[["text_type", "text", "sentiment", "sentiment_score"]]

# ======================
# GOOGLE SHEETS EXPORT
# ======================
def export_to_sheets(df, sheet_name):
    try:
        creds, _ = default()
        gc = gspread.authorize(creds)
        try:
            spreadsheet = gc.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            spreadsheet = gc.create(sheet_name)
        worksheet = spreadsheet.get_worksheet(0)
        worksheet.clear()

        data = [df.columns.tolist()] + df.astype(str).values.tolist()
        worksheet.update(data, value_input_option="USER_ENTERED")
        worksheet.format("A1:D1", {"textFormat": {"bold": True}})
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
    except Exception as e:
        return f"Export Error: {str(e)}"

# Export results
sheet_url = export_to_sheets(df, "US Aid Cuts Sentiment Analysis")
print(f"📊 Analysis Complete! Google Sheets Link: {sheet_url}")
