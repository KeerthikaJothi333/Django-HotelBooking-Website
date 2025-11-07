from django.urls import path
from .views import ViewHotels,AddHotel,HotelDetail,EditHotel,RemoveHotel
from .views import EditHotelImage,DelHotelImage
from .views import get_room_price

urlpatterns = [
    path('', ViewHotels.as_view(), name='view_hotels'),
    path('add/',AddHotel.as_view(), name='add_hotel'),
    path('<int:pk>/',HotelDetail.as_view(), name='hotel_details'),
    path('edit/<int:pk>/',EditHotel.as_view(), name='edit_hotel'),
    path('del/<int:pk>/',RemoveHotel.as_view(), name='del_hotel'),
    

    path('image/edit/<int:pk>/',EditHotelImage.as_view(),name='edit_hotel_image'),
    path('image/del/<int:pk>/',DelHotelImage.as_view(), name='del_hotel_image'),


    path('get-room-price/', get_room_price, name='get_room_price'),
]