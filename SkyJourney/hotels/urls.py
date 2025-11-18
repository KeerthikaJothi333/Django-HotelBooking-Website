from django.urls import path
from .views import ViewHotels,AddHotel,HotelDetail,EditHotel,RemoveHotel
from .views import EditHotelImage,DelHotelImage,EditHotelAmenities
from .views import get_room_price, add_review, searchView

from .views import RoomListView, RoomCreateView, RoomUpdateView, RoomDeleteView

urlpatterns = [
    path('', ViewHotels.as_view(), name='view_hotels'),
    path('add/',AddHotel.as_view(), name='add_hotel'),
    path('<int:pk>/',HotelDetail.as_view(), name='hotel_details'),
    path('edit/<int:pk>/',EditHotel.as_view(), name='edit_hotel'),
    path('del/<int:pk>/',RemoveHotel.as_view(), name='del_hotel'),
    

    path('image/edit/<int:pk>/',EditHotelImage.as_view(),name='edit_hotel_image'),
    path('image/del/<int:pk>/',DelHotelImage.as_view(), name='del_hotel_image'),
    path('hotel/<int:pk>/edit-amenities/', EditHotelAmenities.as_view(), name='edit_hotel_amenities'),

    path('review/<int:booking_id>/',add_review, name='add_review'),

    path('search/', searchView, name = 'search_products'),



    path('get-room-price/', get_room_price, name='get_room_price'),


    
     path("rooms/", RoomListView.as_view(), name="room_list"),
    path("rooms/add/", RoomCreateView.as_view(), name="room_create"),
    path("rooms/<int:pk>/edit/", RoomUpdateView.as_view(), name="room_update"),
    path("rooms/<int:pk>/delete/", RoomDeleteView.as_view(), name="room_delete"),
]