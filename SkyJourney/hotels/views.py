from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from .models import Hotel, Amenity, HotelAmenity, HotelImage


# Create your views here.
from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView
)
from .forms import HotelImageForm
class AddHotel(CreateView):
    model =Hotel
    fields = '__all__'
    template_name = 'hotels/add_hotel.html'
    success_url = reverse_lazy("view_hotels")


class ViewHotels(ListView):
    model = Hotel
    template_name = 'hotels/hotels.html'
    context_object_name = 'hotels'

class HotelDetail(DetailView):
    model = Hotel
    template_name = 'hotels/hotel_details.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] =HotelImageForm()
        return context
    
    def post(self,request,pk):
        this_hotel = Hotel.objects.get(id = pk)
        form = HotelImageForm(request.POST, request.FILES)
        this_hotel_image = form.save(commit=False)
        this_hotel_image.hotel = this_hotel
        this_hotel_image.save()
        return redirect('hotel_details',pk=pk)

class EditHotel(UpdateView):
    model = Hotel
    fields = '__all__'
    template_name = 'hotels/edit_hotel.html'
    success_url = reverse_lazy("view_hotels")

class RemoveHotel(DeleteView):
    model = Hotel
    template_name = 'hotels/del_hotel.html'
    success_url = reverse_lazy("view_hotels")

class EditHotelImage(UpdateView):
    model = HotelImage
    template_name = 'hotels/edit_hotel_image.html'
    form_class=HotelImageForm
    
    def get_success_url(self):
        hotel_pk = self.object.hotel.pk
        return reverse_lazy('hotel_details',kwargs={'pk': hotel_pk})
        

class DelHotelImage(DeleteView):
    model = HotelImage
    template_name = 'hotels/del_hotel_image.html'


    def get_success_url(self):
        hotel_pk = self.object.hotel.pk
        return reverse_lazy('hotel_details',kwargs={'pk': hotel_pk})
        

