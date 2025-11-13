from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Booking
from hotels.models import Room, Hotel, Pricing

from .forms import BookingForm

# 🧾 List all bookings (staff or user-specific)
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # Staff can see all bookings; users see only their own
        if self.request.user.is_staff:
            return Booking.objects.all().order_by('-booked_at')
        return Booking.objects.filter(user=self.request.user).order_by('-booked_at')



class AddBooking(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/add_booking.html'

    def dispatch(self, request, *args, **kwargs):
        self.hotel = get_object_or_404(Hotel, id=self.kwargs['hotel_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['hotel'] = self.hotel
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        room_type = form.cleaned_data['room_type']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # ✅ Assign available room
        available_room = Booking.assign_available_room(
            hotel=self.hotel,
            room_type=room_type,
            start_date=start_date,
            end_date=end_date
        )

        if not available_room:
            messages.error(self.request, "No available rooms for this room type in the selected date range.")
            return redirect('add_booking', hotel_id=self.hotel.id)

        # ✅ Assign the room
        form.instance.room = available_room

        # ✅ Calculate total price
        pricing = Pricing.objects.filter(room_type=room_type).first()
        base_price = pricing.base_price if pricing else 0
        nights = (end_date - start_date).days or 1
        total_price = base_price * nights

        form.instance.total_price = total_price

        # ✅ Save booking first (so we get a booking.id)
        booking = form.save()

        messages.success(self.request, f"Booking created successfully! Proceed to payment (Total: ₹{total_price})")

        # 🔁 Redirect to Razorpay payment page
        return redirect(reverse('payment:create_razorpay_order', args=[booking.id]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = self.hotel
        return context



# 📄 Booking detail view
class BookingDetail(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'booking/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        user = self.request.user

        # Staff can see all bookings
        if user.is_staff:
            return Booking.objects.all()

        # Manager can see bookings of their hotel
        if hasattr(user, 'manager_profile'):
            return Booking.objects.filter(room__hotel=user.manager_profile.hotel)

        # Normal users can only see their own bookings
        return Booking.objects.filter(user=user)
    

# ✏️ Edit/Update booking
class EditBooking(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Booking
    fields = ['start_date', 'end_date', 'status']
    template_name = 'booking/booking_form.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        # model.clean() will handle overlap and date validation
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Booking updated successfully!")
            return response
        except Exception as e:
            messages.error(self.request, f"Update failed: {e}")
            return redirect('booking_update', pk=self.object.pk)

    def test_func(self):
        booking = self.get_object()
        return self.request.user == booking.user or self.request.user.is_staff or self.request.user.manager_profile.hotel == booking.room.hotel


# ❌ Delete booking
class RemoveBooking(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'booking/del_booking.html'
    success_url = reverse_lazy('booking_list')

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, "Booking deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        booking = self.get_object()
        return self.request.user == booking.user or self.request.user.is_staff or self.request.user.manager_profile.hotel == booking.room.hotel
