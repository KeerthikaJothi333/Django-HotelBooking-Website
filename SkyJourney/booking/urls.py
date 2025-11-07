from django.urls import path
from .views import BookingListView,AddBooking,BookingDetail,EditBooking,RemoveBooking




urlpatterns = [
    path('',BookingListView.as_view(), name='booking_list'),
    path('add/<int:hotel_id>/', AddBooking.as_view(), name='add_booking'),
    path('booking/<int:pk>/',BookingDetail.as_view(), name='booking_details'),
    path('booking/edit/<int:pk>/',EditBooking.as_view(), name='edit_booking'),
    path('booking/del/<int:pk>/',RemoveBooking.as_view(), name='del_booking'),
]