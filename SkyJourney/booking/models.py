from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from hotels.models import Room
from datetime import date

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField(default = 0)

    def clean(self):
        # Validate date order
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")

        if self.start_date and self.start_date < date.today():
            raise ValidationError("Start date cannot be in the past.")

        # Validate room overlap
        if self.room_id:
            overlapping = Booking.objects.filter(
                room=self.room,
                status__in=['pending', 'completed']
            ).exclude(id=self.id).filter(
                start_date__lte=self.end_date,
                end_date__gte=self.start_date
            )
            if overlapping.exists():
                raise ValidationError("This room is already booked for the selected dates.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Room {self.room.id} | Hotel {self.room.hotel.name} booked by {self.user.username}"

    class Meta:
        ordering = ['-booked_at']
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    # ✅ New Class Method: Assign room automatically based on hotel, room type, and dates
    @classmethod
    def assign_available_room(cls, hotel, room_type, start_date, end_date):
        """
        Finds the first available room of the given type in the hotel for the date range.
        Returns a Room instance or None.
        """
        rooms = Room.objects.filter(
            hotel=hotel,
            room_type=room_type,
            status='available'
        )

        for room in rooms:
            if room.is_available_for(start_date, end_date):
                return room
        return None
