from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://ai-medical-diagnosis-five.vercel.app"])

# Load API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set in .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

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

        if not hasattr(response, "text") or not response.text.strip():
            return jsonify({
                "error": "No Gemini response",
                "raw": "Gemini returned empty or invalid response"
            }), 502

        clean_text = re.sub(r"^```json|```$", "", response.text.strip(), flags=re.MULTILINE)
        structured = json.loads(clean_text)

        return jsonify(structured)

    except json.JSONDecodeError:
        return jsonify({
            "error": "⚠️ Gemini response could not be parsed.",
            "raw": response.text
        }), 500

    except Exception as e:
        return jsonify({
            "error": str(e),
            "raw": response.text if 'response' in locals() and hasattr(response, 'text') else "No Gemini response"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
