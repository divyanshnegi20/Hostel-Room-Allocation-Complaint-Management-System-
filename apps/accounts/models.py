from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with hostel-specific fields."""

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('warden', 'Warden'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    parent_phone = models.CharField(max_length=15, blank=True, verbose_name='Parent/Guardian Phone')
    address = models.TextField(blank=True)
    institution = models.CharField(max_length=200, blank=True, verbose_name='College/Institution')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_hostel_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_warden(self):
        return self.role == 'warden'
