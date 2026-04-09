from django.contrib import admin
from .models import FeeStructure, Payment


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'is_ac', 'amount', 'fee_period')
    list_filter = ('room_type', 'is_ac', 'fee_period')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'student', 'amount', 'fee_month', 'status', 'payment_date')
    list_filter = ('status', 'fee_month')
    search_fields = ('student__username', 'receipt_number', 'transaction_id')
    readonly_fields = ('transaction_id', 'receipt_number')
