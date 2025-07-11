from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://ai-medical-diagnosis-five.vercel.app"])

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        symptoms = ", ".join(data.get("symptoms", []))
        message = data.get("message", "")

        if not symptoms and not message:
            return jsonify({
                "error": "No symptoms or message provided",
                "raw": "Empty input"
            }), 400

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

        if not response.text.strip():
            return jsonify({
                "error": "No Gemini response",
                "raw": "Gemini returned empty text"
            }), 502

        # Clean and parse Gemini JSON response
        cleaned = re.sub(r"^```json|```$", "", response.text.strip(), flags=re.MULTILINE)
        structured = json.loads(cleaned)

        # Ensure required keys exist
        if all(k in structured for k in ("prediction", "cause", "cure")):
            return jsonify(structured)
        else:
            return jsonify({
                "error": "Missing keys in Gemini response",
                "raw": response.text
            }), 502

    except Exception as e:
        return jsonify({
            "error": str(e),
            "raw": response.text if 'response' in locals() else "No Gemini response"
        }), 500

