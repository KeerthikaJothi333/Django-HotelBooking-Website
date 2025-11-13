from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from .models import Hotel, Amenity, HotelAmenity, HotelImage, Pricing, RoomType


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

from django.utils import timezone

class HotelDetail(DetailView):
    model = Hotel
    template_name = 'hotels/hotel_details.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] =HotelImageForm()

        # ---
        hotel = self.get_object()

        # Show bookings to managers or staff
        if self.request.user.is_staff:
            context['hotel_bookings'] = Booking.objects.filter(room__hotel=hotel, start_date__gte=timezone.now()).order_by('start_date')
        elif hasattr(self.request.user, 'manager_profile'):
            if self.request.user.manager_profile.hotel == hotel:
                context['hotel_bookings'] = Booking.objects.filter(room__hotel=hotel, start_date__gte=timezone.now()).order_by('start_date')
        else:
            context['hotel_bookings'] = None

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

class EditHotelAmenities(UpdateView):
    model = Hotel
    template_name = 'hotels/edit_hotel_amenities.html'
    fields = []  # We'll manage manually
    success_url = reverse_lazy('view_hotels')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all available amenities
        all_amenities = Amenity.objects.all()

        # Get selected amenities for this specific hotel
        selected_amenities = HotelAmenity.objects.filter(hotel=self.object).values_list('amenity_id', flat=True)

        # Debugging (you can comment these after testing)
        print("All amenities:", list(all_amenities.values_list('id', 'title')))
        print("Selected amenities:", list(selected_amenities))

        # Pass to template
        context['all_amenities'] = all_amenities
        context['selected_amenities'] = list(selected_amenities)
        return context

    def post(self, request, *args, **kwargs):
        hotel = self.get_object()
        selected_amenity_ids = request.POST.getlist('amenities')

        # Debugging
        print("POSTed amenities:", selected_amenity_ids)

        # Remove all existing amenities for this hotel
        HotelAmenity.objects.filter(hotel=hotel).delete()

        # Add new amenities
        for amenity_id in selected_amenity_ids:
            try:
                amenity = Amenity.objects.get(id=amenity_id)
                HotelAmenity.objects.create(hotel=hotel, amenity=amenity)
            except Amenity.DoesNotExist:
                pass

        return redirect('view_hotels')


from django.http import JsonResponse

def get_room_price(request):
    room_type_id = request.GET.get('room_type_id')
    print("asdfsadf")
    try:
        room_type = RoomType.objects.get(id=room_type_id)
        pricing = Pricing.objects.filter(room_type=room_type).first()
        if pricing:
            return JsonResponse({'price': pricing.base_price})
        else:
            return JsonResponse({'price': 0})
    except RoomType.DoesNotExist:
        return JsonResponse({'price': 0})
    


# hotels/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import HotelReviewForm
from booking.models import Booking
from .models import HotelReview

@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Prevent duplicate reviews
    if HotelReview.objects.filter(booking=booking, user=request.user).exists():
        messages.warning(request, "You have already reviewed this booking.")
        return redirect('booking_list')

    if request.method == "POST":
        form = HotelReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.booking = booking
            review.save()
            messages.success(request, "Your review has been submitted successfully!")
            return redirect('booking_list')
    else:
        form = HotelReviewForm()

    return render(request, 'hotels/add_review.html', {'form': form, 'booking': booking})


from django.db.models import Q

def searchView(request):
    query = request.GET.get('q')
    result_hotels = Hotel.objects.filter(
        Q(name__icontains=query) |
        Q(location__icontains=query) |
        Q(desc__icontains=query)
    ).distinct()

    context = {
        'query': query,
        'hotels': result_hotels,
        'search_bar': True
    }
    template = 'hotels/search_results.html'

    return render(request, template, context)
