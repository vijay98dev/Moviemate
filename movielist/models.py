from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.

class WatchList (models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey("movielist.StreamPlateform",  on_delete=models.CASCADE ,related_name='watchlist')
    avg_rating = models.FloatField(default=0)
    number_ratings = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    
class StreamPlateform(models.Model):
    name= models.CharField( max_length=50)
    about = models.CharField( max_length=150)
    website = models.URLField( max_length=200)
    
    def __str__(self):
        return self.name
    
    
class Review(models.Model):
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description =models.CharField(max_length=200,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField( auto_now=True)
    active = models.BooleanField(default=True)
    watchlist =models.ForeignKey("movielist.WatchList",  on_delete=models.CASCADE , related_name='reviews')
    review_user =models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return str(self.ratings) + ' | ' + self.watchlist.title + ' | ' + str(self.review_user)
    
    
    