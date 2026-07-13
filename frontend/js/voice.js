/* voice.js — Web Speech API voice input for chat */

let recognition = null;
let isListening = false;
const voiceBtn = document.getElementById('voiceBtn');

function initVoice() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    if (voiceBtn) voiceBtn.title = 'Voice not supported in this browser';
    return null;
  }
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;

  const langMap = {
    'en': 'en-IN', 'hi': 'hi-IN', 'mr': 'mr-IN', 'ta': 'ta-IN',
    'te': 'te-IN', 'kn': 'kn-IN', 'gu': 'gu-IN', 'bn': 'bn-IN',
  };

  recognition.onstart = () => {
    isListening = true;
    voiceBtn.classList.add('listening');
    voiceBtn.innerHTML = '&#x1F534;';
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
      chatInput.value = transcript;
      chatInput.focus();
    }
  };

  recognition.onend = () => {
    isListening = false;
    voiceBtn.classList.remove('listening');
    voiceBtn.innerHTML = '&#x1F3A4;';
  };

  recognition.onerror = (event) => {
    console.warn('Voice error:', event.error);
    isListening = false;
    voiceBtn.classList.remove('listening');
    voiceBtn.innerHTML = '&#x1F3A4;';
  };

  return recognition;
}

function toggleVoice() {
  if (!recognition) initVoice();
  if (!recognition) {
    alert('Voice input is not supported in this browser. Please use Chrome or Edge.');
    return;
  }

  if (isListening) {
    recognition.stop();
  } else {
    const langSelect = document.getElementById('langSelectChat') || document.getElementById('langSelect');
    if (langSelect) {
      const langMap = {
        'en': 'en-IN', 'hi': 'hi-IN', 'mr': 'mr-IN', 'ta': 'ta-IN',
        'te': 'te-IN', 'kn': 'kn-IN', 'gu': 'gu-IN', 'bn': 'bn-IN',
      };
      recognition.lang = langMap[langSelect.value] || 'en-IN';
    }
    recognition.start();
  }
}

// Initialize on load
if (voiceBtn) initVoice();
