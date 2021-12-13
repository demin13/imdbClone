from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist.api import serializers
from watchlist import models

class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='1234')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='netflix', about='#1OTT platform', website = 'https://www.netflix.com')

    def test_streamplatform_create(self):
        data = {
            "name":"Netflix",
            "about": "#1 OTT platform",
            "website":"https://www.netflix.com"
        }
        response = self.client.post(reverse('stream-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse('stream-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
    

class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='1234')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='netflix', about='#1OTT platform',\
                                                            website = 'https://www.netflix.com')
        self.watchlist = models.WatchList.objects.create(title='abc', description='xyz', active=True, platform=self.stream)

    def test_watchlist_create(self):
        data = {
              "title" : "Abc",
              "description": "Two brothers movie",
              "active": True,
              "platform":self.stream,
        }

        response = self.client.post(reverse('Watch-list'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_list(self):
        response = self.client.get(reverse('Watch-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(reverse('WatchList-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'abc')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='1234')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name='netflix', about='#1OTT platform',\
                                                            website = 'https://www.netflix.com')
        self.watchlist = models.WatchList.objects.create(title='abc', description='xyz', active=True, platform=self.stream)
        self.watchlist1 = models.WatchList.objects.create(title="abcd", description="ajks", active=True, platform=self.stream)
        self.review = models.Review.objects.create(owner=self.user, rating=8, comments='any', watchlist=self.watchlist1, active=True)

    def test_review_create(self):
        data = {
            "owner":self.user,
            "rating" : 8,
            "comments":"best nice movie!",
            "watchlist" : self.watchlist,
            "active": True
        }

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            "owner":self.user,
            "rating" : 8,
            "comments":"best nice movie!",
            "watchlist" : self.watchlist,
            "active": True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_review_update(self):

        data = {
            "owner":self.user,
            "rating" : 8,
            "comments":"best nice movie!",
            "watchlist" : self.watchlist,
            "active": True
        }

        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):

        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_indiv(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get('/watch/review?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)