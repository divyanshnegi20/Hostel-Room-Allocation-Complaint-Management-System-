from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'student', 'category', 'priority', 'status', 'created_at')
    list_filter = ('status', 'category', 'priority')
    search_fields = ('subject', 'description', 'student__username', 'student__first_name')
    readonly_fields = ('created_at', 'updated_at')
