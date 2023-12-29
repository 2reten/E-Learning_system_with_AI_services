from django.contrib import admin
from .models import Lecture, Lecture_Programs

class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 1  # 기본적으로 1개의 강좌 입력 필드 제공

class Lecture_ProgramsAdmin(admin.ModelAdmin):
    inlines = [LectureInline]
    list_display = ('title', 'description')  # 목록에 표시될 필드
    search_fields = ['title', 'description']  # 검색 가능한 필드

admin.site.register(Lecture_Programs, Lecture_ProgramsAdmin)
 # Lecture도 별도로 관리자 페이지에 등록
