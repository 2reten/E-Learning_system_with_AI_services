import random
import pandas as pd
from google.cloud import texttospeech
import os
from django.views.decorators.csrf import csrf_exempt

# TensorFlow 환경 변수 설정
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'



from django.shortcuts import render
@csrf_exempt
def pre_interview(request):
        return render(request, 'pre_interview.html')


from .questions import Q1, Q2, Q3, Q4  # 질문 리스트 임포트
import requests

from django.http import JsonResponse
from django.conf import settings
from datetime import datetime
import os
import cv2
import numpy as np
from PIL import Image
from io import BytesIO


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # 업로드된 이미지 파일 받기
        image_file = request.FILES['image']

        # PIL을 사용하여 이미지 읽기
        image = Image.open(image_file)

               # 파일 저장 경로 설정
        face_save_path = os.path.join(settings.MEDIA_ROOT, 'captured_image.jpg')

        # OpenCV를 사용하여 이미지 파일 저장
        cv2.imwrite(face_save_path, cv_image)

        return JsonResponse({'message': '이미지 업로드 및 저장 성공'})
    return JsonResponse({'message': '이미지 업로드 실패'})





@csrf_exempt
def interview_home(request):
    # 면접 페이지 로딩 시 질문 추출 및 음성 파일 생성
    Q_list = [Q1[0], Q1[1], Q2, Q3, Q4]
    question_list = []
    # Q1[0]에서 1개, Q1[1]에서 2개, Q2에서 3개, Q3에서 3개, Q4에서 2개 질문을 선택
    question_list.extend(random.sample(Q_list[0], 1))  # Q1[0]에서 1개
    question_list.extend(random.sample(Q_list[1], 2))  # Q1[1]에서 2개
    question_list.extend(random.sample(Q_list[2], 3))  # Q2에서 3개
    question_list.extend(random.sample(Q_list[3], 3))  # Q3에서 3개
    question_list.extend(random.sample(Q_list[4], 2))  # Q4에서 2개

    # 세션에 질문 리스트 저장
    request.session['interview_questions'] = question_list

    # 콘솔에 질문 출력 및 CSV로 저장
    print(question_list)
    df = pd.DataFrame({'questions': question_list})
    df.to_csv('server_questions.csv', index=False)

    # Google Text-to-Speech API 설정
    client = texttospeech.TextToSpeechClient()
    voice = texttospeech.VoiceSelectionParams(
        language_code='ko-KR', ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    audio_urls = []
    # 질문을 음성 파일로 변환 및 저장
    for i, question in enumerate(question_list):
        synthesis_input = texttospeech.SynthesisInput(text=question)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        # 음성 파일 저장 경로 설정
        filename = f"question_{i + 1}.mp3"
        save_path = os.path.join(settings.MEDIA_ROOT, filename)
        with open(save_path, "wb") as out:
            out.write(response.audio_content)

        # 음성 파일 URL 추가
        audio_url = request.build_absolute_uri(settings.MEDIA_URL + filename)
        audio_urls.append(audio_url)

    # 클라이언트에 전달할 데이터에 오디오 URL 목록 추가
    context = {
        'question_list': question_list,
        'audio_urls': audio_urls
    }

    return render(request, 'interview.html', context)



@csrf_exempt
def start_interview(request):
    if request.method == 'POST':
        try:
            # 세션에서 질문 리스트 가져오기
            question_list = request.session.get('interview_questions', [])

            # 질문 목록을 JSON으로 반환
            return JsonResponse({'questions': question_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)




# 장고서버에 녹음된 오디오를 받아 처이하는 로직
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        if audio_file:
            # 파일 이름을 동적으로 설정합니다.
            file_name = audio_file.name
            save_path = os.path.join(settings.BASE_DIR, 'uploads', file_name)

            with open(save_path, 'wb+') as file:
                for chunk in audio_file.chunks():
                    file.write(chunk)

            # 파일 쓰기가 모두 끝난 후에 성공 메시지를 반환합니다.
            return JsonResponse({'success': True, 'file_path': save_path})
        else:
            return JsonResponse({'success': False, 'error': 'No file uploaded'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})





from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2
import numpy as np
from PIL import Image
import os
import logging
from datetime import datetime
from keras.preprocessing.image import load_img, img_to_array



model = None
def get_emotion_model():
    """Load and return the emotion model."""
    global model
    if model is None:
        model_path = os.path.join(settings.BASE_DIR, 'emotion_model.h5')
        model = load_model(model_path)
    return model

def get_stare_model():
    """Load and return the emotion model."""
    global model
    if model is None:
        model_path = os.path.join(settings.BASE_DIR, 'stare_model.h5')
        model = load_model(model_path)
    return model


from datetime import datetime
import os


# 모델 로딩 및 감정 분석 함수
@csrf_exempt
def analyze_emotion(request):
    model1 = get_emotion_model()  # 모델 로드 (이 부분은 별도로 정의되어 있어야 함)
    model2= get_stare_model()
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            pil_image = Image.open(image_file).convert('RGB')
            open_cv_image = np.array(pil_image)[:, :, ::-1].copy()  # Convert RGB to BGR

            # 얼굴 탐지
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(open_cv_image, 1.1, 4)

            if len(faces) == 0:
                return JsonResponse({'error': 'No faces detected'}, status=400)

            emotions = []
            stares=[]
            for (x, y, w, h) in faces:
                # 얼굴 사이즈 체크
                if w >= 100 and h >= 100:
                    face_img = open_cv_image[y:y+h, x:x+w]
                    resized_img = cv2.resize(face_img, (64, 64))

                    # 이미지 저장
                    face_save_path = os.path.join(settings.MEDIA_ROOT, 'faces', f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpg')
                    if not os.path.exists(os.path.dirname(face_save_path)):
                        os.makedirs(os.path.dirname(face_save_path))
                    cv2.imwrite(face_save_path, resized_img)

                    # 감정 분석
                    img = load_img(face_save_path, target_size=(64, 64))
                    img_array = img_to_array(img) / 255.0
                    img_array = np.expand_dims(img_array, axis=0)

                    ############################
                    predictions = model1.predict(img_array)
                    class_index = np.argmax(predictions[0])
                    emotion_labels = ["Surprise", "Sad", "Happy", "Angry", "Sick", "Confident"]
                    emotion = emotion_labels[class_index]
                    emotions.append(emotion)
                    # print(emotion)
                    predictions2 = model2.predict(img_array)
                    class_index2 = np.argmax(predictions2[0])
                    stare_labels = ["Stare O", "Stare X"]
                    stare = stare_labels[class_index2]
                    stares.append(stare)

                    # 감정 데이터 저장
                    emotion_data_path = os.path.join(settings.BASE_DIR, 'emotion_data.csv')
                    with open(emotion_data_path, 'a') as file:
                        file.write(f'{datetime.now()},{emotion}\n')

                    # 화면응시 데이터 저장
                    stare_data_path = os.path.join(settings.BASE_DIR, 'stare_data.csv')
                    with open(stare_data_path, 'a') as file:
                        file.write(f'{datetime.now()},{stare}\n')

                else:
                    print("Detected face is too small")
            return JsonResponse({'emotions': emotions})


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


