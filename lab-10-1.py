import requests
import pyttsx3
import pyaudio
import wave
import json
import os
import vosk
import sys
from PIL import Image

# Инициализация голосового движка
engine = pyttsx3.init()

# Установка голоса
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Инициализация распознавания речи
model = vosk.Model("C:/vosk-model-small-ru-0.22")
rec = vosk.KaldiRecognizer(model, 16000)

# Функция для произнесения текста
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Функция для записи аудио
def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "audio.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Говорите...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print(result['text'])

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Функция для выполнения команды
def execute_command(command):
    if command == "показать":
        # Получение случайной картинки с сайта
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        url = response.json()['message']

        # Отображение картинки
        os.system(f"start {url}")

    elif command == "сохранить":
        # Сохранение картинки как файл
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        url = response.json()['message']
        os.system(f"start {url}")
        response = requests.get(url)

        with open("dog.jpg", "wb") as f:
            f.write(response.content)

    elif command == "следующая":
        # Обновление картинки
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        url = response.json()['message']

        # Отображение картинки
        os.system(f"start {url}")

    elif command == "назвать породу":
        # Получение породы из ссылки
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        url = response.json()['message']
        os.system(f"start {url}")
        breed = url.split("/")[-2]

        # Произнесение породы
        speak(f"Порода собаки на картинке - {breed}")

    elif command == "разрешение":
        # Получение разрешения картинки
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        url = response.json()['message']
        os.system(f"start {url}")
        response = requests.get(url)

        with open("dog.jpg", "wb") as f:
            f.write(response.content)

        with Image.open("dog.jpg") as img:
            width, height = img.size

        # Произнесение разрешения
        speak(f"Разрешение картинки - {width} на {height} пикселей")
        
    elif command == "стоп":
        sys.exit()

    else:
        speak("Команда не распознана")

# Основной цикл программы
while True:
    record_audio()
    with open("audio.wav", "rb") as f:
        data = f.read()
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            command = result['text'].lower()
            print(command)
            execute_command(command)