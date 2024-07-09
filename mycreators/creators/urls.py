from django.urls import path
from .views import CreatorListView, CreatorAboutMeView
from . import views

urlpatterns = [
    path('', views.CreatorListView.as_view(), name='creator_list'),
    path('creator/<int:pk>/', views.CreatorAboutMeView.as_view(), name='creator_aboutme'),
    path('follow/<int:pk>/', views.follow_creator, name='follow_creator'),
    path('unfollow/<int:pk>/', views.unfollow_creator, name='unfollow_creator'),
    path('following/', views.FollowedCreatorsView.as_view(), name='followed_creators'),
    path('feed/', views.PersonalizedFeedView.as_view(), name='personalized_feed'),
]