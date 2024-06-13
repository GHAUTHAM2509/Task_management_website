// Define a function to initialize timer functionality for each container
function initializeTimer(container) {
    let interval;
    let isPaused = false;
    let title = container.querySelector('.timer1 #title').innerHTML;
    let hours = container.querySelector('.time-display #hours').innerHTML;
    let minutes = container.querySelector('.time-display #minutes').innerHTML;
    let seconds = 0;
    let ini_hours = container.querySelector('.time-display #hours').innerHTML;
    let ini_minutes = minutes = container.querySelector('.time-display #minutes').innerHTML;
    let ini_seconds = 0;

    // Display initial time
    container.querySelector('.time-display #hours').innerHTML = hours.toString().padStart(2, '0');
    container.querySelector('.time-display #minutes').innerHTML = minutes.toString().padStart(2, '0');
    container.querySelector('.time-display #seconds').innerHTML = seconds.toString().padStart(2, '0');


    container.querySelector('.buttons #start').addEventListener('click', () => {
        isPaused = false; // Update isPaused to false when start button is clicked
        start();
    });

    container.querySelector('.buttons #pause').addEventListener('click', pause);
    container.querySelector('.buttons #reset').addEventListener('click', reset);

    function start() {
        // Change button visibility
        container.querySelector('.buttons #start').style.display = "none";
        container.querySelector('.buttons #pause').style.display = "block";
        container.querySelector('.buttons #reset').style.display = "block";

        // Initialize time if not paused
        if (!isPaused) {
            hours = parseInt(container.querySelector('.time-display #hours').innerHTML, 10);
            minutes = parseInt(container.querySelector('.time-display #minutes').innerHTML, 10);
            seconds = parseInt(container.querySelector('.time-display #seconds').innerHTML, 10);
        }

        // Countdown function
        let timerFunction = () => {
            if (isPaused) return;

            // Update the display
            container.querySelector('.time-display #hours').innerHTML = hours.toString().padStart(2, '0');
            container.querySelector('.time-display #minutes').innerHTML = minutes.toString().padStart(2, '0');
            container.querySelector('.time-display #seconds').innerHTML = seconds.toString().padStart(2, '0');
            updateTimer(title,hours, minutes)

            // Decrease the seconds
            seconds--;

            // Check if the time is up
            if (hours === 0 && minutes === 0 && seconds === -1) {
                clearInterval(interval);
                container.querySelector('.time-display #hours').innerHTML = '00';
                container.querySelector('.time-display #minutes').innerHTML = '00';
                container.querySelector('.time-display #seconds').innerHTML = '00';
                updateTimer(title,hours, minutes)
                return; // Exit the function
            }

            // Reset seconds and decrease minutes if necessary
            if (seconds === -1) {
                if (minutes > 0) {
                    minutes--;
                    seconds = 59;
                } else if (hours > 0) {
                    hours--;
                    minutes = 59;
                    seconds = 59;
                }
            }
        };

        // Start the countdown
        clearInterval(interval); // Clear any existing intervals
        interval = setInterval(timerFunction, 1000); // 1000ms = 1s
    }

    function pause() {
        isPaused = true;
        container.querySelector('.buttons #start').style.display = "block";
        container.querySelector('.buttons #pause').style.display = "none";
    }

    function reset() {
        clearInterval(interval);
        hours = 1;
        minutes = 0;
        seconds = 0;
        isPaused = false;
        container.querySelector('.time-display #hours').innerHTML =  ini_hours.toString().padStart(2, '0');;
        container.querySelector('.time-display #minutes').innerHTML =  ini_minutes.toString().padStart(2, '0');
        container.querySelector('.time-display #seconds').innerHTML =  ini_seconds.toString().padStart(2, '0');
        container.querySelector('.buttons #start').style.display = "block";
        container.querySelector('.buttons #pause').style.display = "none";
        container.querySelector('.buttons #reset').style.display = "none";



    }
}

function updateTimer(title,hours, minutes) {
    // Send AJAX request to Flask server to update time in database
    fetch('/update_timer', {
        method: 'POST',
        body: JSON.stringify({title:title, hours: hours, minutes: minutes }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update time in database');
        }
        return response.json();
    })
    .catch(error => {
        console.error('Error updating time in database:', error);
    });
}


// Call initializeTimer function for each timer container
document.querySelectorAll('.timer-container .timer').forEach(timer => {
    initializeTimer(timer);
});
