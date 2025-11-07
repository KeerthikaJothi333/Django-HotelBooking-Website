from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Booking
from hotels.models import RoomType, Room


class BookingForm(forms.ModelForm):
    date_range = forms.CharField(
    label="Select Date Range",
    required=True,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'date_range',
        'id': 'date_range',
        'autocomplete': 'off',
        'placeholder': 'Select your stay dates'
    }))

    room_type = forms.ModelChoiceField(
        queryset=RoomType.objects.all(),
        label="Room Type",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'room_type']
        widgets = {
            'start_date': forms.HiddenInput(),
            'end_date': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.hotel = kwargs.pop('hotel', None)
        super().__init__(*args, **kwargs)

        if self.hotel:
            available_room_types = RoomType.objects.filter(
                room__hotel=self.hotel,
                room__status='available'
            ).distinct()

            self.fields['room_type'].queryset = available_room_types
            self.fields['room_type'].label_from_instance = (
                lambda obj: f"{obj.name} ({Room.objects.filter(hotel=self.hotel, room_type=obj, status='available').count()} available)"
            )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if not end_date:
            end_date = start_date
            
        if not start_date or not end_date:
            raise ValidationError("Please select a valid date range.")

        if start_date < date.today():
            self.add_error('start_date', "Start date cannot be in the past.")
        if end_date < start_date:
            self.add_error('end_date', "End date cannot be before start date.")

        return cleaned_data
