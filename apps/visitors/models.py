from django.db import models
from django.conf import settings


class VisitorEntry(models.Model):
    """Tracks visitors to the hostel."""

    RELATION_CHOICES = [
        ('parent', 'Parent'),
        ('guardian', 'Guardian'),
        ('sibling', 'Sibling'),
        ('friend', 'Friend'),
        ('relative', 'Relative'),
        ('other', 'Other'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visitor_entries')
    visitor_name = models.CharField(max_length=100)
    visitor_phone = models.CharField(max_length=15)
    relation = models.CharField(max_length=15, choices=RELATION_CHOICES, default='parent')
    purpose = models.CharField(max_length=200)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)
    id_proof = models.CharField(max_length=100, blank=True, help_text='ID proof number')
    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='logged_visitors'
    )

    class Meta:
        ordering = ['-check_in']
        verbose_name_plural = 'Visitor Entries'

    def __str__(self):
        return f"{self.visitor_name} → {self.student.get_full_name()} ({self.check_in.strftime('%d/%m/%Y')})"

    @property
    def is_checked_out(self):
        return self.check_out is not None
