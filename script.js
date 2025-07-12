document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const message = document.getElementById('message').value;

    const symptoms = Array.from(document.querySelectorAll('input[name="symptoms"]:checked')).map(cb => cb.value);

    const loader = document.getElementById('loader');
    const resultBox = document.getElementById('result');

    loader.style.display = 'block';
    resultBox.style.display = 'none';

    fetch('https://ai-diagnosis-backend-5aa0.onrender.com/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, age, gender, symptoms, message })
    })
    .then(res => res.json())
    .then(result => {
        const resultBox = document.getElementById('result');
        resultBox.style.display = 'block';

        if (result.prediction && result.cause && result.cure) {
            resultBox.innerHTML = `
                <h3>🩺 Predicted Diagnosis</h3>
                <p>${result.prediction}</p>
                <h4>📌 Likely Cause</h4>
                <p>${result.cause}</p>
                <h4>💊 Suggested Cure</h4>
                <p>${result.cure}</p>
            `;
        } else if (result.raw) {
            resultBox.innerHTML = `<p><strong>⚠️ Response couldn't be parsed:</strong></p><pre>${result.raw}</pre>`;
        } else {
            resultBox.innerHTML = `<p><strong>❌ Error:</strong> ${result.error}</p>`;
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error fetching prediction. Is the backend running?");
    });
});
