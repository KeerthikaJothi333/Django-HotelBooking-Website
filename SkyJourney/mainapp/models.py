from django.db import models

# Create your models here.
class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/')
    title = models.CharField(max_length=100)
    caption = models.TextField(max_length=200,null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"Carousal Image :{self.title}"