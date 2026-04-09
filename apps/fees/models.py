import uuid
from django.db import models
from django.conf import settings


class FeeStructure(models.Model):
    """Defines fee amounts per room type."""

    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    room_type = models.CharField(max_length=10)
    is_ac = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('room_type', 'is_ac', 'fee_period')

    def __str__(self):
        ac_label = 'AC' if self.is_ac else 'Non-AC'
        return f"{self.get_room_type_display()} {ac_label} - ₹{self.amount}/{self.fee_period}"

    def get_room_type_display(self):
        return self.room_type.capitalize()


class Payment(models.Model):
    """Tracks fee payments."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_month = models.CharField(max_length=20, help_text='e.g., April 2026')
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=50, unique=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    receipt_number = models.CharField(max_length=20, unique=True, editable=False)
    payment_method = models.CharField(max_length=30, default='Online (Mock)')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment #{self.receipt_number} - {self.student.get_full_name()} - ₹{self.amount}"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        if not self.receipt_number:
            self.receipt_number = f"RCP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
