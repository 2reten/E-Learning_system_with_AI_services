from django.shortcuts import render
from .models import HomePageImage

def home(request):
    image = HomePageImage.objects.first()  # 첫 번째 이미지를 불러옵니다.
    return render(request, 'home.html', {'image': image})
