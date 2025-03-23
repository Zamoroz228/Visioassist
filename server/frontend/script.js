const responseText = document.getElementById('responseText');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const uploadPreview = document.getElementById('upload-preview');
const uploadPreviewContainer = document.getElementById('upload-preview-container');
const loader = document.getElementById('loader');
const speechOption = document.getElementById('speechOption');
const pauseResumeBtn = document.getElementById('pauseResumeBtn');
const stopBtn = document.getElementById('stopBtn');
const speechControls = document.querySelector('.speech-controls');

let speechSynthesis = window.speechSynthesis;
let speechUtterance = null;
let isSpeaking = false;
let isPaused = false;

fileInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        uploadPreview.src = URL.createObjectURL(file);
        uploadPreviewContainer.style.display = 'block';
        uploadBtn.disabled = false;
    }
});

const uploadArea = document.querySelector('.upload-area');
uploadArea.addEventListener('dragover', function(event) {
    event.preventDefault();
    uploadArea.classList.add('active');
});

uploadArea.addEventListener('dragleave', function() {
    uploadArea.classList.remove('active');
});

uploadArea.addEventListener('drop', function(event) {
    event.preventDefault();
    uploadArea.classList.remove('active');

    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        fileInput.files = event.dataTransfer.files;
        uploadPreview.src = URL.createObjectURL(file);
        uploadPreviewContainer.style.display = 'block';
        uploadBtn.disabled = false;
    }
});

uploadBtn.addEventListener('click', function() {
    const file = fileInput.files[0];
    if (file) {
        sendToServer(file);
    }
});

function sendToServer(file) {
    const mode = document.querySelector('input[name="mode"]:checked').value;
    stopSpeech();
    
    responseText.textContent = "Обработка изображения...";
    loader.style.display = 'block';
    speechControls.style.display = 'none';

    const formData = new FormData();
    formData.append('image', file);
    formData.append('mode', mode);
    const serverURL = "http://91.77.167.51:5000/process_image";
    const xhr = new XMLHttpRequest();
    xhr.open('POST', serverURL, true);
    
    xhr.onload = function() {
        loader.style.display = 'none';
        
        if (xhr.status === 200) {
            try {
                const data = JSON.parse(xhr.responseText);
                
                if (data && data.result) {
                    responseText.textContent = data.result;
                    
                    if (speechOption.checked) {
                        speakText(data.result);
                        speechControls.style.display = 'flex';
                    }
                } else if (data && data.error) {
                    responseText.textContent = "Ошибка: " + data.error;
                } else {
                    responseText.textContent = "Получен пустой или некорректный ответ от сервера";
                }
            } catch (e) {
                responseText.textContent = "Ошибка при обработке ответа сервера";
            }
        } else {
            responseText.textContent = `Ошибка сервера: ${xhr.status}`;
        }
    };
    
    xhr.onerror = function() {
        loader.style.display = 'none';
        responseText.textContent = "Ошибка соединения с сервером";
    };
    
    xhr.send(formData);
}

function speakText(text) {
    if (!speechSynthesis) return;
    
    stopSpeech();
    
    speechUtterance = new SpeechSynthesisUtterance(text);
    speechUtterance.lang = 'ru-RU';
    
    speechUtterance.onend = function() {
        isSpeaking = false;
        isPaused = false;
        pauseResumeBtn.textContent = 'Пауза';
        speechControls.style.display = 'none';
    };
    
    speechSynthesis.speak(speechUtterance);
    isSpeaking = true;
}

function pauseResumeSpeech() {
    if (!speechSynthesis || !speechUtterance) return;
    
    if (isSpeaking && !isPaused) {
        speechSynthesis.pause();
        isPaused = true;
        pauseResumeBtn.textContent = 'Продолжить';
    } else if (isPaused) {
        speechSynthesis.resume();
        isPaused = false;
        pauseResumeBtn.textContent = 'Пауза';
    }
}

function stopSpeech() {
    if (!speechSynthesis) return;
    
    speechSynthesis.cancel();
    isSpeaking = false;
    isPaused = false;
    pauseResumeBtn.textContent = 'Пауза';
}

pauseResumeBtn.addEventListener('click', pauseResumeSpeech);
stopBtn.addEventListener('click', stopSpeech);

function openTab(event, tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });

    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    document.getElementById(tabName).style.display = 'block';
    event.currentTarget.classList.add('active');

    responseText.textContent = "Здесь появится результат обработки...";
    stopSpeech();
    speechControls.style.display = 'none';
    
    if (tabName === 'lastPhoto') {
        loadLastProcessedImage();
    }
}

function loadLastProcessedImage() {
    const lastImageElement = document.getElementById('last-processed-image');
    lastImageElement.src = "http://91.77.167.51:5000/last_image?" + new Date().getTime();
    lastImageElement.style.display = 'block'
}
