from django.db import models
from django.conf import settings


class Room(models.Model):
    """Represents a hostel room."""

    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('dormitory', 'Dormitory'),
    ]

    room_number = models.CharField(max_length=20, unique=True)
    floor = models.PositiveIntegerField(default=1)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default='double')
    total_beds = models.PositiveIntegerField(default=2)
    is_ac = models.BooleanField(default=False, verbose_name='Air Conditioned')
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['floor', 'room_number']

    def __str__(self):
        return f"Room {self.room_number} (Floor {self.floor})"

    @property
    def available_beds(self):
        return self.beds.filter(status='available').count()

    @property
    def occupied_beds(self):
        return self.beds.filter(status='occupied').count()

    @property
    def is_full(self):
        return self.available_beds == 0

    @property
    def occupancy_percentage(self):
        total = self.beds.count()
        if total == 0:
            return 0
        return round((self.occupied_beds / total) * 100)


class Bed(models.Model):
    """Represents a bed within a room."""

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_label = models.CharField(max_length=10, help_text='e.g., A, B, C')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')

    class Meta:
        unique_together = ('room', 'bed_label')
        ordering = ['room', 'bed_label']

    def __str__(self):
        return f"Bed {self.bed_label} - Room {self.room.room_number}"


class Allocation(models.Model):
    """Tracks student-to-bed allocation."""

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='allocations')
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name='allocations')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    allocated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='allocations_made'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.get_full_name()} → {self.bed}"

    def save(self, *args, **kwargs):
        # Update bed status based on allocation
        if self.is_active:
            self.bed.status = 'occupied'
        else:
            # Check if there's another active allocation for this bed
            other_active = Allocation.objects.filter(
                bed=self.bed, is_active=True
            ).exclude(pk=self.pk).exists()
            if not other_active:
                self.bed.status = 'available'
        self.bed.save()
        super().save(*args, **kwargs)
