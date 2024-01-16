
from django.shortcuts import get_object_or_404, render
from .models import Course
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CourseForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def is_instructor(user):
    return user.userprofile.is_instructor

@login_required
@user_passes_test(is_instructor)
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # 강좌 목록 페이지로 리다이렉트
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect(course.get_absolute_url())
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.userprofile.is_instructor:
        courses = Course.objects.filter(instructor=request.user)
    else:
        # 학생의 경우 관련 로직 추가 (현재 예제에는 학생과 강좌를 연결하는 로직이 없음)
        courses = []  # 현재 예제에서는 학생의 경우 비어있는 리스트로 설정
    return render(request, 'courses/dashboard.html', {'courses': courses})


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.students.add(request.user)
    return redirect('courses:dashboard')