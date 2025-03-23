# 🔍 VisioAssist

## 🌟 Интеллектуальный помощник для слабовидящих и незрячих

VisioAssist — это инновационное решение, разработанное для помощи людям с нарушениями зрения в восприятии визуальной информации. Проект состоит из веб-приложения и специализированного устройства на базе Raspberry Pi 5, обеспечивающих доступ к технологиям компьютерного зрения.

### 🎯 Цель проекта

Создать доступный инструмент, который позволит слабовидящим и незрячим людям "видеть" окружающий мир через технологии искусственного интеллекта и машинного обучения.

## ✨ Основные функции

### 📱 Устройство (Raspberry Pi 5)
- **OCR**: Распознавание и чтение текста с фотографий
- **Генерация описаний**: Создание подробных словесных описаний изображений
- **Голосовой интерфейс**: Озвучивание всей информации с помощью SilleroTTS
- **Двухкнопочное управление**: Отдельные кнопки для OCR и генерации описаний

### 💻 Веб-приложение (visioassist.ru)
- **OCR**: Распознавание текста с загруженных изображений
- **Генерация описаний**: Автоматическое создание подписей к изображениям
- **Просмотр истории**: Отображение последнего обработанного изображения
- **Голосовой вывод**: Озвучивание результатов через Web Speech API

## 🛠️ Технический стек

### 🖥️ Серверная часть
```
flask                # Веб-фреймворк
flask_cors           # Поддержка кросс-доменных запросов
PIL                  # Обработка изображений
torch                # Фреймворк для машинного обучения
torchvision          # Библиотека компьютерного зрения
transformers         # Модели для обработки естественного языка
cv2                  # Компьютерное зрение
numpy                # Математические операции
pytesseract (ru,en)  # OCR движок
tqdm                 # Индикаторы прогресса
```

### 🍓 Raspberry Pi 5
```
requests             # HTTP запросы
picamera2            # Работа с камерой Raspberry Pi
lqpio                # Управление GPIO
torch                # Фреймворк для машинного обучения
soundfile            # Обработка аудиофайлов
pygame               # Воспроизведение звука
pathlib              # Работа с путями файловой системы
cv2                  # Компьютерное зрение
pytesseract (ru,en)  # OCR движок
SilleroTTS           # Система синтеза речи
```

## 🚀 Установка и запуск

### Серверная часть
```bash
# Клонирование репозитория
git clone https://github.com/yourusername/visioassist.git

# Запуск фронтенда
cd frontend
python -m http.server 8000

# Запуск бэкенда (в отдельном терминале)
cd backend
python.exe main.py
```

### Устройство (Raspberry Pi 5)
```bash
# На Raspberry Pi
.../.venv/bin/python .../main.py
```

## 📖 Использование

### Веб-приложение
1. Откройте браузер и перейдите на сайт [visioassist.ru](https://visioassist.ru)
2. Загрузите изображение, перетащив его в соответствующую область
3. Выберите режим обработки: OCR или генерация описания
4. При необходимости включите озвучивание результатов
5. Нажмите кнопку "Отправить фото"
6. Результат обработки отобразится на экране

### Устройство
1. Включите устройство VisioAssist, нажав кнопку питания
2. Дождитесь завершения загрузки системы (будет голосовое уведомление)
3. Наведите камеру на объект или текст
4. Для распознавания текста нажмите кнопку OCR
5. Для получения описания изображения нажмите кнопку описания
6. Устройство автоматически обработает изображение и озвучит результат

---

# 🔍 VisioAssist

## 🌟 Intelligent Assistant for Visually Impaired and Blind People

VisioAssist is an innovative solution designed to help people with visual impairments perceive visual information. The project consists of a web application and a specialized device based on Raspberry Pi 5, providing access to computer vision technologies.

### 🎯 Project Goal

Create an accessible tool that allows visually impaired and blind people to "see" the world around them through artificial intelligence and machine learning technologies.

## ✨ Key Features

### 📱 Device (Raspberry Pi 5)
- **OCR**: Recognition and reading of text from photographs
- **Description Generation**: Creation of detailed verbal descriptions of images
- **Voice Interface**: Vocalization of all information using SilleroTTS
- **Two-button Control**: Separate buttons for OCR and description generation

### 💻 Web Application (visioassist.ru)
- **OCR**: Text recognition from uploaded images
- **Description Generation**: Automatic creation of captions for images
- **History Viewing**: Display of the last processed image
- **Voice Output**: Vocalization of results through Web Speech API

## 🛠️ Technology Stack

### 🖥️ Server Side
```
flask                # Web framework
flask_cors           # Cross-domain request support
PIL                  # Image processing
torch                # Machine learning framework
torchvision          # Computer vision library
transformers         # Natural language processing models
cv2                  # Computer vision
numpy                # Mathematical operations
pytesseract (ru,en)  # OCR engine
tqdm                 # Progress indicators
```

### 🍓 Raspberry Pi 5
```
requests             # HTTP requests
picamera2            # Raspberry Pi camera interface
lqpio                # GPIO management
torch                # Machine learning framework
soundfile            # Audio file processing
pygame               # Sound playback
pathlib              # File system path operations
cv2                  # Computer vision
pytesseract (ru,en)  # OCR engine
SilleroTTS           # Speech synthesis system
```

## 🚀 Installation and Launch

### Server Side
```bash
# Clone the repository
git clone https://github.com/yourusername/visioassist.git

# Launch frontend
cd frontend
python -m http.server 8000

# Launch backend (in a separate terminal)
cd backend
python.exe main.py
```

### Device (Raspberry Pi 5)
```bash
# On Raspberry Pi
.../.venv/bin/python .../main.py
```

## 📖 Usage

### Web Application
1. Open your browser and go to [visioassist.ru](https://visioassist.ru)
2. Upload an image by dragging it to the appropriate area
3. Select the processing mode: OCR or description generation
4. If needed, enable result vocalization
5. Click the "Submit Photo" button
6. The processing result will be displayed on the screen

### Device
1. Turn on the VisioAssist device by pressing the power button
2. Wait for the system to boot up (there will be a voice notification)
3. Point the camera at an object or text
4. For text recognition, press the OCR button
5. For image description, press the description button
6. The device will automatically process the image and vocalize the result
