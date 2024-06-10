from django.db import models

# Create your models here.

class WatchList (models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey("movielist.StreamPlateform",  on_delete=models.CASCADE ,related_name='watchlist')
    
    def __str__(self):
        return self.title
    
    
class StreamPlateform(models.Model):
    name= models.CharField( max_length=50)
    about = models.CharField( max_length=150)
    website = models.URLField( max_length=200)
    
    def __str__(self):
        return self.name