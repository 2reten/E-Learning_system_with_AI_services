from django.shortcuts import render, get_object_or_404
from .models import Lecture_Programs

def lecture_programs_list(request):
    programs = Lecture_Programs.objects.all()
    return render(request, 'lecture_programs_list.html', {'programs': programs})

def lecture_program_detail(request, pk):
    program = get_object_or_404(Lecture_Programs, pk=pk)
    return render(request, 'lecture_program_detail.html', {'program': program})