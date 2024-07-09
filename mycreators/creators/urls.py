from django.urls import path
from .views import CreatorListView

urlpatterns = [
    path('', CreatorListView.as_view(), name='creator_list'),
]