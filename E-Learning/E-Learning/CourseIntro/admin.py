from django.contrib import admin
from .models import CourseIntro

@admin.register(CourseIntro)
class CourseIntroAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
