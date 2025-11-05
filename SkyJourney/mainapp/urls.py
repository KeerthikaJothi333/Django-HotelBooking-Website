#URL routing for mainapp
from django.urls import path
from .views import homeView,aboutView,contactView
from .views import ViewCarouselImages, AddCarouselImage,EditCarousel,RemoveCarousel
urlpatterns = [
    path('',homeView, name='home_page'),
    path('carousel/all/', ViewCarouselImages.as_view(), name='carousel_page'),
    path('carousel/add/', AddCarouselImage.as_view(), name='add_carousel'),
    path('carousel/edit/<int:pk>', EditCarousel.as_view(), name='edit_carousel'),
    path('carousel/del/<int:pk>', RemoveCarousel.as_view(), name='del_carousel'),
    

    path('about', aboutView, name='about_page'),
    path('contact', contactView, name='contact_page')
]