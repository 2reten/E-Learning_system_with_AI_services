from django.shortcuts import render
from homedesign.models import HomePageImage
from CourseIntro.models import CourseIntro

def home(request):
    images = HomePageImage.objects.all()  # 모든 HomePageImage 객체를 가져옵니다.
    course_intros = CourseIntro.objects.all()  # 모든 CourseIntro 객체를 가져옵니다.
    context = {
        'images': images,
        'course_intros': course_intros,
    }
    return render(request, 'home.html', context)

def index(request):
    return render(request, 'home.html')

#CourseIntro의 상세 페이지를 보여주는 뷰
def courseintro_detail(request, slug):
    course_intro = get_object_or_404(CourseIntro, slug=slug)
    return render(request, 'courseintro_detail.html', {'course_intro': course_intro})


def search(request):
    query = request.GET.get('q', '')
    # 검색 결과를 담을 리스트
    results = []

    if query:
        courses = Course.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        questions = Question.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        courses = Course.objects.none()
        questions = Question.objects.none()

    context = {
        'courses': courses,
        'questions': questions,
        'query': query,
        'results': results,
    }

    return render(request, 'search_results.html', context)


def board_manage(request):
    # 함수 로직...
    return render(request, 'board_manage.html')

def interview(request):
    return render(request, 'interview.html')