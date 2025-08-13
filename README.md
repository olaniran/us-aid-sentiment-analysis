# US Foreign Aid Freeze 2025 - Sentiment Analysis
Sentiment and Thematic Analysis of US Foreign Aid Narratives
This repository contains the Python script and resources for the manuscript titled "Sentiment and Thematic Analysis of Narratives Surrounding US Foreign Aid Cuts and Their Impact on Global Health". The project uses Natural Language Processing (NLP) to analyze news articles, specifically focusing on the sentiment and thematic elements related to the impact of US aid policies on global health crises.

##📜 Project Overview
This project employs a dual-analysis approach to dissect textual data from news articles. It combines two powerful pre-trained transformer models to perform:

Sentiment Analysis: To determine the emotional tone (Positive, Neutral, Negative) of the text.

Zero-Shot Thematic Classification: To categorize the text into predefined theoretical themes without requiring specific training examples for those themes.

The primary goal is to systematically evaluate how narratives surrounding US aid cuts are framed, providing empirical data on public and media sentiment and the dominant themes discussed. The final output is neatly organized and exported to a Google Sheet for further review and analysis.

##✨ Features
Dual-Model Pipeline: Integrates twitter-roberta-base-sentiment for robust sentiment analysis and bart-large-mnli for flexible zero-shot thematic classification.

Custom Thematic Labels: Easily define and modify a list of themes relevant to your research focus.

Google Colab Ready: Includes authentication helpers for seamless execution in a Google Colab environment.

Automated Google Sheets Export: Automatically processes the text and exports the results to a new or existing Google Sheet, providing a shareable and accessible output.

Structured Output: Generates a clean pandas DataFrame containing the original text, sentiment scores, and primary/secondary thematic classifications.

##🚀 Getting Started
Follow these instructions to set up and run the analysis on your own machine or in Google Colab.

Prerequisites
Python 3.6+

A Google account (for Google Colab and Google Sheets integration)

Installation
Clone the repository:

Bash

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
Install the required Python packages:
The script is designed to install dependencies automatically using pip. The core packages are:

Bash

pip install --upgrade gspread transformers pandas torch torchaudio
Running in Google Colab (Recommended)
Open the Notebook: Upload the .py script or create a new Colab notebook and paste the code.

Authentication: When you run the cell containing auth.authenticate_user(), a pop-up window will appear. Follow the prompts to grant the notebook access to your Google account. This is necessary for exporting data to Google Sheets.

Run All Cells: Execute the cells in order to perform the analysis and generate the Google Sheet link.

###🔧 How to Use
1. Configure the Analysis
Before running the script, you can customize the analysis parameters.

Sentiment Labels: The SENTIMENT_LABELS dictionary maps the model's output to human-readable labels. These are generally fixed based on the model used.

Python

SENTIMENT_LABELS = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive",
}
Theoretical Labels: Modify the THEORY_LABELS list to reflect the themes you want to investigate.

Python

THEORY_LABELS = [
    "Impact on healthcare delivery",
    "Impact on humanitarian aid",
    "Impact on WHO operations",
    "Impact on disease surveillance",
    "Impact on conflict zones",
]
2. Input Your Data
The sample data is structured as a Python dictionary. Replace the title and narratives with the text you wish to analyze.

Python

article = {
    "title": "Your article title here",
    "narratives": [
        "First paragraph or key sentence.",
        "Second paragraph or key sentence.",
        # Add as many narratives as needed
    ],
}
3. Run the Script
Execute the Python script. It will:

Initialize the sentiment and zero-shot classification models.

Analyze the title and each narrative.

Compile the results into a pandas DataFrame.

Authenticate with your Google account.

Export the DataFrame to a Google Sheet.

4. View the Output
Upon successful execution, a link to the Google Sheet will be printed in the console.

##📊 Analysis Complete! Google Sheets Link: https://docs.google.com/spreadsheets/d/your-sheet-id
The sheet will contain the following columns:

text_type: Whether the text is the Title or a Narrative.

text: The original text segment.

sentiment: The predicted sentiment (Positive, Negative, Neutral).

sentiment_score: The confidence score (0 to 1) for the sentiment prediction.

primary_theory: The theme with the highest score above a 0.25 threshold.

primary_score: The confidence score for the primary theme.

secondary_theory: The theme with the second-highest score.

secondary_score: The confidence score for the secondary theme.

##🤖 Models Used
This project relies on two state-of-the-art models from the Hugging Face Hub:

Sentiment Analysis: cardiffnlp/twitter-roberta-base-sentiment

A RoBERTa-base model fine-tuned on a massive dataset of tweets, making it highly effective for analyzing sentiment in news and social media text.

Zero-Shot Classification: facebook/bart-large-mnli

A BART-large model fine-tuned on the Multi-Genre Natural Language Inference (MNLI) corpus. It can classify text into arbitrary labels without having been explicitly trained on them, making it perfect for flexible thematic analysis.

##🤝 Contributing
Contributions are welcome! If you have suggestions for improving the code, adding features, or expanding the analysis, please feel free to open an issue or submit a pull request.

Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Make your changes.

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/your-feature-name).

Open a Pull Request.

