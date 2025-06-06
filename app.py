from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    name = data.get('name', 'User')
    symptoms = data.get('symptoms', [])

    diagnosis = "Symptoms unclear or not enough data"
    cause = "The provided symptoms don't match any known conditions in the system."
    cure = "Please provide more details or consult a healthcare professional."

    
    if "fever" in symptoms and "cold" in symptoms:
        diagnosis = f"{name}, you may have Flu or a viral infection"
        cause = "Likely due to viral infection caused by seasonal viruses or exposure to infected individuals."
        cure = "Rest, stay hydrated, take paracetamol, and consult a doctor if fever persists more than 3 days."
    elif "headache" in symptoms and "vision" in symptoms:
        diagnosis = f"{name}, you may be experiencing a migraine or eye strain"
        cause = "May be due to stress, dehydration, prolonged screen time, or uncorrected vision problems."
        cure = "Take rest, reduce screen time, drink water, and consider seeing an eye specialist."
    elif "high bp" in symptoms:
        diagnosis = f"{name}, you may have High Blood Pressure"
        cause = "Often caused by poor diet, lack of exercise, stress, or genetics."
        cure = "Reduce salt, exercise daily, avoid stress, and consult a doctor for medication."
    elif "low sugar" in symptoms:
        diagnosis = f"{name}, you have Low Blood Sugar (Hypoglycemia)"
        cause = "May occur due to missed meals, excessive insulin, or strenuous activity without eating."
        cure = "Consume fast sugar (juice, glucose), rest, and monitor blood sugar levels."
    elif "bloating" in symptoms:
        diagnosis = f"{name}, you may have Gastric Bloating or Indigestion"
        cause = "Commonly caused by overeating, gas-producing foods, or slow digestion."
        cure = "Avoid oily food, drink warm water, try antacids, and eat light meals."
    elif "throat pain" in symptoms:
        diagnosis = f"{name}, you may have a Throat Infection or Sore Throat"
        cause = "Usually caused by viral or bacterial infection, or irritation from pollution or allergens."
        cure = "Gargle with salt water, stay hydrated, and avoid spicy food. Use lozenges or see a doctor if it worsens."
    elif "skin problem" in symptoms:
        diagnosis = f"{name}, you may have a skin condition"
        cause = "Could be due to allergies, infections, or irritants."
        cure = "Keep skin clean, avoid irritants, and seek dermatological advice."
    else:
        diagnosis = "Symptoms unclear or not enough data"
        cause = "The provided symptoms don't match any known conditions in the system."
        cure = "Please provide more details or consult a healthcare professional."
    return jsonify({
    'prediction': diagnosis,
    'cause': cause,
    'cure': cure
})


if __name__ == '__main__':
    app.run(debug=True)
