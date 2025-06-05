document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault(); // prevent the form from reloading the page

    const name = document.getElementById('name').value;
    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const message = document.getElementById('message').value;

    // Get all checked symptoms
    const symptoms = Array.from(document.querySelectorAll('input[name="symptoms"]:checked')).map(cb => cb.value);

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, age, gender, symptoms, message })
    })
    .then(res => res.json())
    .then(result => {
        const resultBox = document.getElementById('result');
        resultBox.style.display = 'block';
       resultBox.innerHTML = `
    <h3>Predicted Diagnosis:</h3>
    <p>${result.prediction}</p>
    <h4>Likely Cause:</h4>
    <p>${result.cause}</p>
    <h4>Suggested Cure:</h4>
    <p>${result.cure}</p>
`;

    })
    .catch(err => {
        console.error(err);
        alert("Error fetching prediction. Is the backend running?");
    });
});



