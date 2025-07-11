from flask import Flask, request, jsonify  
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        symptoms = ", ".join(data.get("symptoms", []))
        message = data.get("message", "")
        
        prompt = f"""
A patient reports the following symptoms: {symptoms}.
Additional notes: {message}.

🩺 Provide:
1. A short diagnosis (1–2 lines)
2. Likely cause
3. Suggested cure

Respond ONLY in this exact JSON format:
{{
  "prediction": "...",
  "cause": "...",
  "cure": "..."
}}
"""

        response = model.generate_content(prompt)

        # Clean response from Markdown formatting
        clean_text = re.sub(r"^```json|```$", "", response.text.strip(), flags=re.MULTILINE)
        structured = json.loads(clean_text)

        return jsonify(structured)

    except Exception as e:
        return jsonify({"error": str(e), "raw": response.text}), 500

if __name__ == "__main__":
    app.run(debug=True)
