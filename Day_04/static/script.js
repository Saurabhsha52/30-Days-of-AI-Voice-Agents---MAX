// static/js/script.js

// --- Text-to-Speech Section ---
const textInput = document.getElementById('tts-input');
const generateButton = document.getElementById('generate-button');
const ttsAudio = document.getElementById('tts-audio');

generateButton.addEventListener('click', async () => {
    const text = textInput.value;
    if (!text) {
        alert("Please enter some text!");
        return;
    }
    
    try {
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


// --- Echo Bot Section ---
const startRecordingBtn = document.getElementById('start-recording-btn');
const stopRecordingBtn = document.getElementById('stop-recording-btn');
const playbackAudio = document.getElementById('playback-audio');

let mediaRecorder;
let audioChunks = [];

async function getMicrophoneAccess() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        return stream;
    } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Permission to access microphone was denied.');
        return null;
    }
}

startRecordingBtn.addEventListener('click', async () => {
    const stream = await getMicrophoneAccess();
    if (!stream) return;
    
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(audioBlob);
        playbackAudio.src = audioUrl;
        playbackAudio.play();
    };

    mediaRecorder.start();
    startRecordingBtn.disabled = true;
    stopRecordingBtn.disabled = false;
    console.log("Recording started...");
});

stopRecordingBtn.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        startRecordingBtn.disabled = false;
        stopRecordingBtn.disabled = true;
        console.log("Recording stopped.");
    }
});