from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from movielist import models
from movielist.api import serializers

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user= User.objects.create_user(username='exmaple',password='password@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream= models.StreamPlateform.objects.create(name='Netflix',about='straming platform',
                                                               website='https://netflix.com')
    
    def test_streamplatform_create(self):
        data={
            'name':'Netflix',
            'about': 'streaming platform',
            'website': 'https://netflix.com',
        }
        response= self.client.post(reverse('streamplatform-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response=self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_stramplateform_list_ind(self):
        response=self.client.get(reverse('streamplatform-detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
        
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username='example',password='password@123')
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream= models.StreamPlateform.objects.create(name='Netflix',about='straming platform',website='https://netflix.com')
        self.watchlist= models.WatchList.objects.create(platform=self.stream,title='exmaple Movie',storyline='Exmaple story',active=True)
    def test_watchlist_create(self):
        data={
            'paltform':self.stream,
            'title':'exmaple Movie',
            'storyline':'Exmaple story',
            'active':True
        }
        response= self.client.post(reverse('movie-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response= self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        response= self.client.get(reverse('movie-details',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
class ReviewTestCase(APITestCase):
    def setUp (self):
        self.user=User.objects.create_user(username='example',password='password@123')
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream= models.StreamPlateform.objects.create(name='Netflix',about='straming platform',website='https://netflix.com')
        self.watchlist= models.WatchList.objects.create(platform=self.stream,title='exmaple Movie',storyline='Exmaple story',active=True)
        self.watchlist2= models.WatchList.objects.create(platform=self.stream,title='exmaple Movie',storyline='Exmaple story',active=True)
        self.review=models.Review.objects.create(review_user=self.user,ratings=5,description='Greate Movie',watchlist=self.watchlist2,active=True)
        
    def test_review_create(self):
        data={
            'review_user':self.user,
            'ratings':5,
            'description':'Great Movie',
            'watchlist':self.watchlist,
            'active':True,
        }
        response= self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
    def test_review_create_unauth(self):
        data={
            'review_user':self.user,
            'ratings':5,
            'description':'Great Movie',
            'watchlist':self.watchlist,
            'active':True,
        }
        self.client.force_authenticate(user=None)
        response= self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        data={
            'review_user':self.user,
            'ratings':4,
            'description':'Great Movie - Updated',
            'watchlist':self.watchlist,
            'active':False,
        }
        response= self.client.put(reverse('review-details',args=(self.review.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_review_list(self):
        response= self.client.get(reverse('review-list',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_review_ind(self):
        response=self.client.get(reverse('review-details',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_review_delete(self):
        response=self.client.delete(reverse('review-details',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        
    def test_review_user(self):
        response=self.client.get('/watch/reviews/?username'+self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)