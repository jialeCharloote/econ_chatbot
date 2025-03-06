from flask import Flask, request, jsonify, render_template
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.json
    title = data.get('title', '')
    description = data.get('description', '')
    ticker = data.get('ticker', '')
    
    # Create the prompt
    prompt = f"""You are a financial analyst in a leading hedge fund. 
Analyze the sentiment of the following financial news for the given stock ticker step by step.
Title: "{title}"
Summary: "{description}"
Stock Ticker: {ticker}
Step 1: Identify key financial terms and their implications.
Step 2: Determine whether the news suggests market optimism, pessimism, or neutrality for this specific stock.
Step 3: Based on your analysis, classify the sentiment into one of the following categories:
- "Bullish": If the news suggests confidence, growth, or positive impact on this stock.
- "Bearish": If the news suggests decline, risks, or negative impact on this stock.
- "Neutral": If the news is ambiguous or does not convey strong sentiment.
Finally, **return only** the final result in valid JSON format, with the structure:
{{
  "ticker": "{ticker}",
  "sentiment": "Bullish" | "Bearish" | "Neutral",
  "sentiment_reasoning": "Provide a brief explanation of the sentiment analysis."
}}"""

    # Call the Hugging Face API with your fine-tuned model
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.1,
            "max_length": 1024
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        
        # Hugging Face API can return different response formats
        # We need to handle both list and dictionary formats
        if isinstance(result, list):
            result_text = result[0].get('generated_text', '')
        elif isinstance(result, dict):
            # Check if there's an error
            if "error" in result:
                return jsonify({"error": result["error"]}), 400
            result_text = result.get('generated_text', '')
        else:
            result_text = str(result)
        
        return jsonify({"response": result_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)