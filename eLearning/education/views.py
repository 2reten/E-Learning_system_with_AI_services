from django.shortcuts import render
from .models import Lecture_Programs
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404

def education_home(request):
    return render(request, 'education_home.html')


# 강좌 프로그램 리스트를 JSON으로 보여주는 뷰
def lecture_programs_list(request):
    programs = Lecture_Programs.objects.all()
    programs_json = serializers.serialize('json', programs)
    return JsonResponse(programs_json, safe=False)

# 각 강좌 프로그램의 세부 강의를 보여주는 뷰
def lecture_detail(request, pk):
    program = get_object_or_404(Lecture_Programs, pk=pk)
    lectures = program.lectures.all()
    return render(request, 'lecture_detail.html', {'program': program,  'lectures': lectures})

