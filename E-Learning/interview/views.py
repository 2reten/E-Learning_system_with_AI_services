from django.shortcuts import render
from django.http import JsonResponse
import random
from .questions import questions

def interview_home(request):
    return render(request, 'interview.html')

def start_interview(request):
    if request.method == 'POST':
        selected_questions = random.sample(questions, 5)
        return JsonResponse({'questions': selected_questions})
    # POST 요청이 아닐 경우, 오류 메시지를 보냅니다.
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


