from django.urls import path, include
from . import views
from .views import(
    IndexView,
)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('creator/edit/', views.EditCreatorAboutMeView.as_view(), name='edit_creator_aboutme'),
    path('creator/delete/', views.DeleteCreatorAccount.as_view(), name='delete_creator_account'),
    path('creator/<str:username>/', views.CreatorAboutMeView.as_view(), name='creator_aboutme'),
    path('creator-status/', views.creator_status, name='creator_status'),
    path('follow/<int:pk>/', views.follow_creator, name='follow_creator'),
    path('unfollow/<int:pk>/', views.unfollow_creator, name='unfollow_creator'),
    path('following/', views.FollowedCreatorsView.as_view(), name='followed_creators'),
    path('feed/', views.PersonalizedFeedView.as_view(), name='personalized_feed'),
    path('creators/', views.CreatorListView.as_view(), name='creator_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('request-creator/', views.request_creator_status, name='request_creator_status'),
    path('request-submitted/', views.creator_request_submitted, name='creator_request_submitted'),
    path('approve_creator/<str:username>/', views.approve_creator, name='approve_creator'),
    path('reject_creator/<str:username>/', views.reject_creator, name='reject_creator'),
    path("accounts/", include("allauth.urls")),
    
]