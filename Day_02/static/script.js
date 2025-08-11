async function loadVoices(){
  const status = document.getElementById("status");
  const sel = document.getElementById("voiceSelect");
  status.textContent = "Loading voices...";
  try {
    const res = await fetch("/voices");
    const data = await res.json();
    if (!res.ok) {
      status.textContent = `Error loading voices: ${JSON.stringify(data).slice(0,200)}`;
      return;
    }
    sel.innerHTML = "";
    (Array.isArray(data) ? data : data.voices || []).forEach(v=>{
      const opt = document.createElement("option");
      opt.value = v.id || v.voiceId || v;
      opt.textContent = v.name || v.id || opt.value;
      sel.appendChild(opt);
    });
    status.textContent = "Voices loaded.";
  } catch(err) {
    status.textContent = "Could not fetch voices: " + err.message;
  }
}

async function generateAudio() {
  const text = document.getElementById("ttsText").value.trim();
  const voice = document.getElementById("voiceSelect").value;
  const status = document.getElementById("status");
  const audioPlayer = document.getElementById("audioPlayer");
  const audioElement = document.getElementById("audioElement");
  const raw = document.getElementById("rawResponse");

  if (!text) { alert("Enter text"); return; }
  status.textContent = "Generating audio...";
  raw.textContent = "";
  audioPlayer.classList.add("hidden");

  try {
    const resp = await fetch("/generate-tts", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ text, voiceId: voice, format: "mp3" })
    });
    const data = await resp.json();
    if (resp.ok && data.audio_url) {
      audioElement.src = data.audio_url;
      audioPlayer.classList.remove("hidden");
      status.textContent = "Audio ready ✅";
    } else {
      status.textContent = "Error generating audio — see details below.";
      raw.textContent = JSON.stringify(data, null, 2);
      console.error("Murf error", data);
    }
  } catch (err) {
    status.textContent = "Network / unexpected error: " + err.message;
    console.error(err);
  }
}

document.getElementById("refreshVoices").addEventListener("click", loadVoices);
window.addEventListener("load", loadVoices);