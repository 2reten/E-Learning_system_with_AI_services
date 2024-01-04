import os
import pygame
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
import pyaudio
import io
import cv2
from PIL import Image, ImageTk


def update_video(vid_main, canvas_main, root, photo_holder):
    ret_main, frame_main = vid_main.read()
    if ret_main:
        photo_holder[0] = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame_main, cv2.COLOR_BGR2RGB)))
        canvas_main.create_image(0, 0, image=photo_holder[0], anchor="nw")
    root.after(10, lambda: update_video(vid_main, canvas_main, root, photo_holder))

def update_timer(timer, timer_label, root):
    if timer[0] > 0:
        timer[0] -= 1
        timer_label.configure(text=convert_seconds_to_time(timer[0]))
        root.after(1000, lambda: update_timer(timer, timer_label, root))

def convert_seconds_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02}:{seconds:02}"


# 인증 파일 경로 설정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cellular-fold-400204-e79f7516818e.json"

def play_audio(filename):
    pygame.init()  # pygame 초기화
    pygame.mixer.init()  # mixer (사운드) 초기화
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def record_audio(seconds=5):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = int(RATE / 10)  # 100ms
    audio = io.BytesIO()
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    for _ in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        audio.write(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    audio.seek(0)
    return audio.getvalue()


def write_audio(audio_data):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ko-KR", )
    response = client.recognize(config=config, audio=audio)

    try:
        return response.results[0].alternatives[0].transcript
    except (IndexError, AttributeError):
        return "답변 없음"


def speak(text):
    pygame.mixer.init()  # mixer 초기화
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="ko-KR",
                                              ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)  # 여성 목소리로 수정
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    audio_io = io.BytesIO(response.audio_content)
    pygame.mixer.music.load(audio_io)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


import os
import base64
import fitz
import uuid
import time
import json
import requests
from tkinter import filedialog
import threading

api_url = 'https://b2krob5h4d.apigw.ntruss.com/custom/v1/25145/fc5ba381289e1ea080b42703ffc052645d02bf55f28497f492db77a08d4ecad4/general'
secret_key = 'Tk9VRU9kZ0p1Tk1ZWUV5dWN6dGRLSFpLdmNtZ2pBR1I='
resume = ""

def upload_resume():
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="자소서 선택",
                                           filetypes=(('pdf files', '*.pdf'), ('all files', '*.*')))
    if file_path:  # 사용자가 파일을 선택한 경우
        print(f"선택된 자소서 경로: {file_path}")
        threading.Thread(target=ocr_text, args=(file_path,)).start()


def ocr_text(file_path):
    global resume
    image_data_base64 = base64.b64encode(open(file_path, 'rb').read()).decode('utf-8')
    doc = fitz.open(file_path)
    total_pages = doc.page_count

    for i in range(total_pages):
        page = doc.load_page(i)

        request_json = {
            'images': [{'format': 'pdf', 'name': 'demo', 'data': image_data_base64}],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }

        headers = {'X-OCR-SECRET': secret_key, 'Content-Type': 'application/json'}
        response = requests.post(api_url, headers=headers, data=json.dumps(request_json).encode('utf-8'), timeout=30)
        result = response.json()

        text = ""
        for image_result in result['images']:
            for field in image_result['fields']:
                text += field['inferText']

        retext = text.replace('<', '>').replace('.', '>')
        paragraphs = retext.split('>')

        for paragraph in paragraphs:
            resume += paragraph + "\n"
        print(resume)


