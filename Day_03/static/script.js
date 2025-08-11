// static/js/script.js

console.log("Hello from script.js! The backend is serving this file.");

// Get the HTML elements
const textInput = document.getElementById('tts-input');
const generateButton = document.getElementById('generate-button');
const ttsAudio = document.getElementById('tts-audio');

// Add a click event listener to the button
generateButton.addEventListener('click', async () => {
    const text = textInput.value;
    if (!text) {
        alert("Please enter some text!");
        return;
    }
    
    try {
        // Send a POST request to the backend endpoint
        const response = await fetch('/generate-audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }

        const data = await response.json();
        const audioUrl = data.audio_url;

        // Set the audio element's source and play the audio
        if (audioUrl) {
            ttsAudio.src = audioUrl;
            ttsAudio.play();
        } else {
            alert("Failed to get audio URL from the server.");
        }

    } catch (error) {
        console.error('Error generating audio:', error);
        alert('An error occurred. Check the console for details.');
    }
});