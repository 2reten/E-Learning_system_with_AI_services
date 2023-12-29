from django.db import models

class Lecture_Programs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Lecture(models.Model):
    program = models.ForeignKey(Lecture_Programs, related_name='lectures', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='lectures/videos/')
    description = models.TextField()

    def __str__(self):
        return self.title
