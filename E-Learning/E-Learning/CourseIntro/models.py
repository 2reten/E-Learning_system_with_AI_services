from django.urls import reverse
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.template.defaultfilters import slugify
from PIL import Image, ImageOps

class ResizedImageField(models.ImageField):
    def pre_save(self, model_instance, add):
        file = super(ResizedImageField, self).pre_save(model_instance, add)

        if file and not file.closed:
            img = Image.open(file)
            img = img.convert('RGB')
            # ANTIALIAS를 LANCZOS로 변경
            img.thumbnail((800, 800), Image.LANCZOS)

            buffer = BytesIO()
            img.save(fp=buffer, format='JPEG', quality=85)
            file.file = buffer
            file.name = file.name

        return file



class CourseIntro(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = ResizedImageField(upload_to='course_intros/')
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(CourseIntro, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('courseintro_detail', kwargs={'slug': self.slug})
