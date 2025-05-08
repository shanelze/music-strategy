// record audio
const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const speech_result = document.getElementById("speech_data");
const dot = document.getElementById("dot");

const recognition = new webkitSpeechRecognition();
recognition.lang = window.navigator.language;
recognition.interimResults = true;

startButton.addEventListener("click", () => {
  dot.hidden = false;
  recognition.start();
});
stopButton.addEventListener("click", () => {
  dot.hidden = true;
  recognition.stop();
});

recognition.addEventListener("result", (event) => {
  const result = event.results[event.results.length - 1][0].transcript;
  speech_result.textContent = result;
});
