from django.db import models

class HomePageImage(models.Model):
    image = models.ImageField(upload_to='images/')
    # 추가 필드가 필요하다면 여기에 추가할 수 있습니다.

    def __str__(self):
        return "HomePage Image"


