document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultContainer = document.getElementById('result-container');
    const resultContent = document.getElementById('result-content');
    const loader = document.getElementById('loader');

    analyzeBtn.addEventListener('click', async function() {
        // Get values from inputs
        const ticker = document.getElementById('ticker').value.trim();
        const title = document.getElementById('title').value.trim();
        const description = document.getElementById('description').value.trim();

        // Validate inputs
        if (!ticker || !title || !description) {
            alert('Please fill in all fields');
            return;
        }

        // Show loader
        resultContainer.style.display = 'block';
        resultContent.innerHTML = '';
        loader.style.display = 'block';

        try {
            // Send request to the server
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ticker, title, description })
            });

            const data = await response.json();
            
            // Handle the response
            try {
                const result = JSON.parse(data.response);
                
                // Format the result
                let sentimentClass = '';
                if (result.sentiment === 'Bullish') sentimentClass = 'bullish';
                else if (result.sentiment === 'Bearish') sentimentClass = 'bearish';
                else sentimentClass = 'neutral';
                
                resultContent.innerHTML = `
                    <p><strong>Ticker:</strong> ${result.ticker}</p>
                    <p><strong>Sentiment:</strong> <span class="${sentimentClass}">${result.sentiment}</span></p>
                    <p><strong>Reasoning:</strong> ${result.sentiment_reasoning}</p>
                `;
            } catch (e) {
                // If the response is not valid JSON
                resultContent.innerHTML = `<p>${data.response}</p>`;
            }
        } catch (error) {
            resultContent.innerHTML = `<p>Error: ${error.message}</p>`;
        } finally {
            // Hide loader
            loader.style.display = 'none';
        }
    });
});