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
# MODEL CONFIGURATION
# ======================
SENTIMENT_LABELS = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive",
}

# Define your thematic labels for the BART model
THEORY_LABELS = [
    "Impact on healthcare delivery",
    "Impact on humanitarian aid",
    "Impact on WHO operations",
    "Impact on disease surveillance",
    "Impact on international relations",
]

# Initialize RoBERTa model for sentiment
sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

# Initialize BART model for zero-shot thematic classification
# Set device to GPU (0) if available, otherwise CPU (-1)
device = 0 if torch.cuda.is_available() else -1
theory_model = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=device
)

# ======================
# ANALYSIS FUNCTION
# ======================
def analyze_text(text):
    """
    Run combined sentiment (RoBERTa) and thematic (BART) analysis.
    """
    # 1. Sentiment Analysis
    sentiment_result = sentiment_model(text)[0]
    sentiment_label = SENTIMENT_LABELS.get(sentiment_result["label"], sentiment_result["label"])
    sentiment_score = round(sentiment_result["score"], 3)

    # 2. Thematic Analysis
    try:
        theory_result = theory_model(
            text,
            THEORY_LABELS,
            multi_label=True,
            hypothesis_template="This text discusses {}." # Improves model accuracy
        )
        # Filter theories with a confidence score above a threshold (e.g., 0.25)
        theories = [
            (label, round(score, 3))
            for label, score in zip(theory_result["labels"], theory_result["scores"])
            if score > 0.25
        ]
        # Assign primary and secondary theories
        primary_theory, primary_score = theories[0] if theories else ("N/A", 0.0)
        secondary_theory, secondary_score = theories[1] if len(theories) > 1 else ("N/A", 0.0)

    except Exception as e:
        print(f"Error during thematic analysis: {e}")
        primary_theory, primary_score = "Error", 0.0
        secondary_theory, secondary_score = "Error", 0.0

    return {
        "text": text,
        "sentiment": sentiment_label,
        "sentiment_score": sentiment_score,
        "primary_theory": primary_theory,
        "primary_score": primary_score,
        "secondary_theory": secondary_theory,
        "secondary_score": secondary_score,
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

# Create DataFrame with the new thematic columns
df = pd.DataFrame(results)[[
    "text_type", "text", "sentiment", "sentiment_score",
    "primary_theory", "primary_score", "secondary_theory", "secondary_score"
]]

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
        
        # Update format range to include new columns (A1 to H1)
        worksheet.format("A1:H1", {"textFormat": {"bold": True}})
        
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
    except Exception as e:
        return f"Export Error: {str(e)}"

# Export results to a sheet with a more descriptive name
sheet_url = export_to_sheets(df, "Sentiment and Thematic Analysis of US Aid Cuts")
print(f"📊 Analysis Complete! Google Sheets Link: {sheet_url}")
