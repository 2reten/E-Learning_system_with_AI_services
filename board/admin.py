from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Board, Board_Manage

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'view_on_site')
    search_fields = ('name', 'description')
    list_filter = ('name',)

    def view_on_site(self, obj):
        url = reverse('board:board_detail', kwargs={'board_id': obj.id})
        return format_html("<a href='{}'>View on site</a>", url)

admin.site.register(Board, BoardAdmin)

