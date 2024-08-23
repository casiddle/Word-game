document.addEventListener('DOMContentLoaded', function() {
    const startForm = document.getElementById('start-game-form');
    const gameArea = document.getElementById('game-area');
    const instructions = document.getElementById('instructions');
    const guessInput = document.getElementById('guess');
    const guessButton = document.getElementById('guess-button');
    const feedback = document.getElementById('feedback');
    const guessHistory = document.getElementById("guess-history");
    const giveupButton=document.getElementById("give-up");
    const giveUpModal = document.getElementById('give-up-modal');
    const closeButton = document.getElementById('close-button');
    const giveUpMessage = document.getElementById('give-up-message');
    const closeSpan = document.getElementsByClassName('close')[0];
    const successModal = document.getElementById('successModal');
    const successClose = document.getElementById('successClose');
    const successMessage = document.getElementById('successMessage');

    // Restart the game
    function restartGame() {
        // Reset the game area
        gameArea.style.display = 'none';
        instructions.innerText = '';
        guessHistory.innerHTML = '';
        feedback.innerText = '';
        guessInput.value = '';
    

        startForm.submit();
    }

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
            instructions.innerText = `Guess a word`;
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
            newHistoryItem.innerText = `Guess: ${guess} Result: ${data.result.toUpperCase()}`;

                
            // Prepend the new history item to the top
            guessHistory.insertBefore(newHistoryItem, guessHistory.firstChild);
            
            //clear input field
            guessInput.value="";

            if (data.result === 'correct') {
                successMessage.innerHTML = ` ${data.message}`;
                successModal.style.display = 'block'; // Show the success modal
            }
        })
        .catch(error => {
            console.error('Error making guess:', error);
        });
    });

    // Close modal when the user clicks on <span> (x)
    successClose.addEventListener('click', function() {
        successModal.style.display = 'none'; // Hide the success modal
        restartGame(); // Restart the game after closing the modal
    });

    // Close modal when the user clicks anywhere outside of the modal
    window.addEventListener('click', function(event) {
        if (event.target === successModal) {
            successModal.style.display = 'none'; // Hide the success modal
            restartGame(); // Restart the game after closing the modal
        }
    });

    giveupButton.addEventListener("click", function(){
        // Fetch the word from the server (assuming it's stored in a session or similar)
        fetch('/give_up', {
            method: 'GET',
              })
        .then(response => response.json())
        .then(data => {
             // Display the message in the modal
             giveUpMessage.innerText = `The word was: ${data.word}, you had ${data.counter} guesses before giving up`;
             giveUpModal.style.display = "block";
            })
        .catch(error => {
            console.error('Error giving up:', error);
        });
    });

    // When the user clicks on <span> (x), close the modal
    closeSpan.addEventListener('click', function() {
        giveUpModal.style.display = "none";
        restartGame();
    });

    // When the user clicks the close button, close the modal and restart the game
    closeButton.addEventListener('click', function() {
        giveUpModal.style.display = "none";
        restartGame();
    });

    // When the user clicks anywhere outside of the modal, close it
    window.addEventListener('click', function(event) {
        if (event.target == giveUpModal) {
            giveUpModal.style.display = "none";
            restartGame();
        }
    });



    const alphabet = document.getElementById("alphabetModal")
    const book = document.getElementById("fa-book")

    function bookHover() {
        alphabet.style.display = "block";
    }
    
    function bookNormal() {
        alphabet.style.display = "none";
    }

    book.addEventListener("mouseover", bookHover);
    book.addEventListener("mouseout", bookNormal);


    
});


