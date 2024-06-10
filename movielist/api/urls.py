from django.urls import path
# from movielist.api.views import movie_list,movie_details
from movielist.api.views import WatchListAV,WatchListDetails,StreamPlateformList,StreamPlaterformDetails


urlpatterns = [
    path('list/',WatchListAV.as_view(),name='movie-list'),
    path('<int:pk>/',WatchListDetails.as_view(),name='movie-details'),
    
    path('stream/',StreamPlateformList.as_view(),name='stream'),
    path('stream/<int:pk>/',StreamPlaterformDetails.as_view(),name='stream-details'),
]