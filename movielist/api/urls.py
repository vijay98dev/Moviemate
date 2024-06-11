from django.urls import path,include
# from movielist.api.views import movie_list,movie_details
from movielist.api.views import WatchListAV,WatchListDetails,StreamPlateformList,StreamPlaterformDetails,StreamViewSets,ReviewList,ReviewDetail,ReviewCreate
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('stream',StreamViewSets,basename='streamplatform')

urlpatterns = [
    path('list/',WatchListAV.as_view(),name='movie-list'),
    path('<int:pk>/',WatchListDetails.as_view(),name='movie-details'),
    
    path('',include(router.urls)),
    # path('stream/',StreamPlateformList.as_view(),name='stream'),
    # path('stream/<int:pk>/',StreamPlaterformDetails.as_view(),name='stream-details'),
    
    # path('review/',ReviewList.as_view(),name='review-list'),
    # path('review/<int:pk>/',ReviewDetail.as_view(),name='review-details'),
    path('stream/<int:pk>/review/',ReviewList.as_view(),name='review-list'),
    path('stream/<int:pk>/review-create/',ReviewCreate.as_view(),name='review-list'),
    path('stream/review/<int:pk>/',ReviewDetail.as_view(),name='review-details'),
    
]