document.addEventListener('DOMContentLoaded', function() {
    const startForm = document.getElementById('start-game-form');
    const gameArea = document.getElementById('game-area');
    const instructions = document.getElementById('instructions');
    const guessInput = document.getElementById('guess');
    const guessButton = document.getElementById('guess-button');
    const feedback = document.getElementById('feedback');
    const guessHistory = document.getElementById('guess-history');

    if (!startForm || !gameArea || !instructions || !guessInput || !guessButton || !feedback||!guessHistory) {
        console.error('One or more required elements are missing in the HTML.');
        return;
    }

    // Start game form submission
    startForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const dictionaryChoice = document.getElementById('dictionary_choice').value;

        fetch('/start_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ dictionary_choice: dictionaryChoice })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            gameArea.style.display = 'block';
            instructions.innerText = "Guess a word"; //, word:${data.word}";
            guessHistory.innerHTML="";
            feedback.innerText="";
        })
        .catch(error => {
            console.error('Error starting game:', error);
        });
    });

    // Guess submission
    guessButton.addEventListener('click', function() {
        const guess = guessInput.value;

        if (!guess) {
            alert('Please enter a guess.');
            return;
        }

        fetch('/guess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ guess: guess })
        })
        .then(response => response.json())
        .then(data => {
            feedback.innerText = data.result;
            // Update guess history
            const newHistoryItem = document.createElement('p');
            newHistoryItem.innerText = `Guess: ${guess}, Result: ${data.result.toUpperCase()}`;

                
            // Prepend the new history item to the top
            guessHistory.insertBefore(newHistoryItem, guessHistory.firstChild);
            
            //clear input field
            guessInput.value="";

            if (data.result === 'correct') {
                alert(data.message);
                gameArea.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error making guess:', error);
        });
    });
});

