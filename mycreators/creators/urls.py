from django.urls import path
from .views import CreatorListView, CreatorAboutMeView

urlpatterns = [
    path('', CreatorListView.as_view(), name='creator_list'),
    path('<int:pk>/', CreatorAboutMeView.as_view(), name='creator_aboutme'),
]