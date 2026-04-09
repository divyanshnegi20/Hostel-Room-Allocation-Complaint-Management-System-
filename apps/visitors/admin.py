from django.contrib import admin
from .models import VisitorEntry


@admin.register(VisitorEntry)
class VisitorEntryAdmin(admin.ModelAdmin):
    list_display = ('visitor_name', 'student', 'relation', 'purpose', 'check_in', 'check_out')
    list_filter = ('relation', 'check_in')
    search_fields = ('visitor_name', 'visitor_phone', 'student__username')
