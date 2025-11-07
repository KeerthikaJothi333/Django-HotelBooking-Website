from django.shortcuts import render
from django.urls import reverse_lazy

from .models import CarouselImage

from hotels.models import Hotel

# Create your views here.
def homeView(request):
    template_name = 'mainapp/home.html'
    context ={
        #dictionary with context data.
        'carousel_images' : CarouselImage.objects.all(),
        'hotels' : Hotel.objects.all()
    }
    return render(request, template_name, context)

from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

class AddCarouselImage(CreateView):
    model = CarouselImage # This provides table name for inserting records
    fields = '__all__' # Fields to insert values into
    # Defining where the site should redirect to, after successful insertion of record.
    success_url = reverse_lazy('carousel_page')
    template_name = 'mainapp/add_carousel.html'

class EditCarousel(UpdateView):
    model = CarouselImage
    template_name = 'mainapp/edit_carousel.html'
    fields = '__all__'
    success_url = reverse_lazy('carousel_page')

    
class ViewCarouselImages(ListView):
    model =CarouselImage
    context_object_name = 'carousel_images'
    template_name = 'mainapp/carousel_list.html'

class RemoveCarousel(DeleteView):
    model = CarouselImage
    template_name = 'mainapp/del_carousel.html'
    success_url = reverse_lazy('carousel_page')
    
def aboutView(request):
    template_name = 'mainapp/about.html'
    context ={
        #dictionary with context data.
    }
    return render(request, template_name, context)
    



def contactView(request):
    template_name = 'mainapp/contact.html'
    context ={
        #dictionary with context data.
    }
    return render(request, template_name, context)
