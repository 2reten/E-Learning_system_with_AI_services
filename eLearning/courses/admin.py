
from django.contrib import admin
from .models import Course, UserProfile


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date']
    search_fields = ['title', 'description']


admin.site.register(Course)
admin.site.register(UserProfile)
