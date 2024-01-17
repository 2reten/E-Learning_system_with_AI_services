from django.db import models

class Lecture_Programs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='lecture_programs/images/', default='default_image.jpg')  # 기본값 추가

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Lecture Programs"

class Lecture(models.Model):
    program = models.ForeignKey(Lecture_Programs, related_name='lectures', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='lectures/videos/')
    video.url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title
