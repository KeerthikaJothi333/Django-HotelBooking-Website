from django.forms import ModelForm
from .models import HotelImage

class HotelImageForm(ModelForm):
    class Meta:
        model = HotelImage
        fields = ['img','hotel','category']