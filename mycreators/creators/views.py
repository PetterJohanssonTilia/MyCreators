from django.shortcuts import render
from django.views.generic import ListView
from .models import Creator

# Create your views here.

class CreatorListView(ListView):
    model = Creator
    template_name = 'creators/creator_list.html'
    context_object_name = 'creators'