from django import forms
from .models import HotelImage

class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ['img','hotel','category']



from .models import HotelReview

class HotelReviewForm(forms.ModelForm):
    class Meta:
        model = HotelReview
        fields = ['stars', 'comment']
        widgets = {
            'stars': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'placeholder': 'Rate 1–5'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review...'
            }),
        }