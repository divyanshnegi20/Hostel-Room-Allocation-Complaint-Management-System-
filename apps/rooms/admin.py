from django.contrib import admin
from .models import Room, Bed, Allocation


class BedInline(admin.TabularInline):
    model = Bed
    extra = 0


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'floor', 'room_type', 'total_beds', 'is_ac', 'monthly_rent', 'available_beds')
    list_filter = ('floor', 'room_type', 'is_ac')
    search_fields = ('room_number',)
    inlines = [BedInline]


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('bed_label', 'room', 'status')
    list_filter = ('status', 'room__floor')


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ('student', 'bed', 'start_date', 'end_date', 'is_active', 'allocated_by')
    list_filter = ('is_active', 'start_date')
    search_fields = ('student__username', 'student__first_name', 'bed__room__room_number')
