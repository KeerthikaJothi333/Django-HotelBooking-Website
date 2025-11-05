from django.db import models
from django.urls import reverse

# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='hotels/thumbnails/')
    location = models.CharField(max_length=200)
    desc = models.TextField(null=True ,blank=True)
    contact_number = models.CharField(max_length=15)
    # rating, amenities

    def __str__(self):
        return f"Hotel: {self.name}"
    
    def get_absolute_url(self):
        return reverse("hotel_details", kwargs={"pk": self.pk})
    @property
    def hotel_amenities(self):
        return self.amenity.all()

    @property
    def total_rooms(self):
        """Returns count of total working rooms in hotels."""
        return self.rooms.filter(status='available').count()
    
    @property
    def detail_count(self):
        room_types = RoomType.objects.all()
        data = []
        for room_type in room_types:
            data.append(
                {
                    room_type.name : Room.objects.filter(hotel = self, room_type = room_type, status='available').count()
                }
                )
        print(data)
        return data

    
class HotelImage(models.Model):
    CATEGORY_CHOICES = [
        ('exterior', 'Exterior'),
        ('lobby', 'Lobby'),
        ('room', 'Room'),
        ('suite', 'Suite'),
        ('bathroom', 'Bathroom'),
        ('restaurant', 'Restaurant'),
        ('bar', 'Bar'),
        ('pool', 'Pool'),
        ('spa', 'Spa'),
        ('gym', 'Gym'),
        ('conference', 'Conference Room'),
        ('banquet', 'Banquet Hall'),
        ('parking', 'Parking Area'),
        ('reception', 'Reception'),
        ('view', 'Scenic View'),
        ('garden', 'Garden'),
        ('terrace', 'Terrace'),
        ('kids', 'Kids Zone'),
        ('other', 'Other'),
    ]
    img = models.ImageField(upload_to='hotels/images/')
    hotel = models.ForeignKey(Hotel, related_name='images', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.get_category_display()}"
    def get_absolute_url(self):
        return reverse("hotel_details", kwargs={"pk: self.hotel.pk"})

class Amenity(models.Model): 
    title = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.title}"
    
class HotelAmenity(models.Model):
    """
    Model for Many to Many relation b/w Hotel and Amenity
    """
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, related_name="hotel")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='amenity')

    added_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.amenity.title} at {self.hotel.name}"


# --------------------------------Rooms------------------------------------------------ #
from django.core.exceptions import ObjectDoesNotExist


class RoomType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Pricing(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='pricing_options')
    capacity = models.PositiveIntegerField(default=1)
    base_price = models.PositiveIntegerField()

    class Meta:
        unique_together = ('room_type', 'capacity')

    def __str__(self):
        return f"{self.room_type.name} (Capacity: {self.capacity}) - ₹{self.base_price}"


class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_service', 'Out of Service'),
    ]

    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.room_number} - {self.room_type.name}"

    @property
    def price(self):
        """Return price by finding matching Pricing for this room_type and capacity."""
        try:
            pricing = Pricing.objects.get(room_type=self.room_type, capacity=self.capacity)
            return pricing.base_price
        except ObjectDoesNotExist:
            return None  # or 0 if you prefer default value
