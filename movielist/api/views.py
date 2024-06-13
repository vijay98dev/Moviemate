from movielist.models import WatchList,StreamPlateform,Review
from movielist.api.serializers import WatchListSerializer,StreamPlateformSerializer,ReviewSerializer
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
# from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from movielist.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnly


class WatchListAV(APIView):
    def get(self, request):
        movie = WatchList.objects.all()
        serializer = WatchListSerializer(movie, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = WatchListSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
class WatchListDetails(APIView):
    def get (self,request,pk):
        try:
            movie=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self,request,pk):
        try:
            movie=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie,data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        movie= WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


# class StreamPlateformList(APIView):
    
#     def get(self, request):
#         platform = StreamPlateform.objects.all()
#         serializer = StreamPlateformSerializer(platform,many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = StreamPlateformSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer._errors)


# class StreamPlaterformDetails(APIView):
#     def get(self, request, pk):
#         try:
#             plateform=StreamPlateform.objects.get(pk=pk)
#         except StreamPlateform.DoesNotExist:
#             return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamPlateformSerializer(plateform)
#         return Response (serializer.data)
    
#     def put(self,request,pk):
#         plateform=StreamPlateform.objects.get(pk=pk)
#         serializer=StreamPlateformSerializer(plateform,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     def delete(self , request, pk):
#         plateform=StreamPlateform.objects.get(pk=pk)
#         plateform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class StreamViewSets(viewsets.ViewSet):
    def list(self, request):
        queryset = StreamPlateform.objects.all()
        serializer = StreamPlateformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlateform.objects.all()
        movie = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlateformSerializer(movie)
        return Response(serializer.data)

    def create(self, request):
        serializer = StreamPlateformSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer._errors)
        
    def destroy(self, request, pk=None):
        plateform=StreamPlateform.objects.get(pk=pk)
        plateform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewCreate(generics.CreateAPIView):
    serializer_class =ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist,review_user=review_user)
        print(review_queryset)
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this watchlist')
        if watchlist.number_ratings ==0:
            watchlist.avg_rating = serializer.validated_data['ratings']
        else:
            watchlist.avg_rating =(watchlist.avg_rating + serializer.validated_data['ratings'])/2
            
        watchlist.number_ratings = watchlist.number_ratings+1
        watchlist.save()
        serializer.save(watchlist=watchlist,review_user=review_user)
    
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    
# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get (self, request, *args, **kwargs):
#         return self.retrieve(request,*args, **kwargs)
    
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request,*args, **kwargs)
    
#     def post(self,request,*args, **kwargs):
#         return self.create(request,*args, **kwargs)


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movie = Movie.objects.all()
#         serializer = MovieSerializer(movie, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request,pk):
#     if request.method == 'GET':
#         movie = Movie.objects.get(id=pk)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(id=pk)
#         serializer = MovieSerializer(movie,data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
        
#     if request.method == 'DELETE':
#         movie= Movie.objects.get(id=pk)
#         movie.delete()
#         return Response(status=204)