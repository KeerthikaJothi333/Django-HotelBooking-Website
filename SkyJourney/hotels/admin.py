from django.contrib import admin

# Register your models here.
from .models import Hotel, Amenity, HotelAmenity, HotelImage


admin.site.register(Hotel)
admin.site.register(Amenity)
admin.site.register(HotelAmenity)
admin.site.register(HotelImage)


# ------
from .models import Room, RoomType, Pricing
admin.site.register([RoomType, Room, Pricing])