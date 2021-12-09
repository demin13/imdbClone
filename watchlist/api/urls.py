from django.urls import path
from .views import (WatchListView, WatchDetailView, StreamPlatformListView,
                    StreamPlatformDetailView, ReviewListView, ReviewDetailView, ReviewCreateView)

urlpatterns = [
    path('list/', WatchListView.as_view(), name='Watch-list'),
    path('list/<int:pk>/', WatchDetailView.as_view(), name='WatchList-detail'),
    path('stream/', StreamPlatformListView.as_view(), name='stream-list'),
    path('stream/<int:pk>/', StreamPlatformDetailView.as_view(), name='stream-detail'),

    path('<int:pk>/review-create/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/review/', ReviewListView.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail')
]