from django.shortcuts import render
from django.views.generic import ListView
from .models import Creator
from django.db.models import Q


# Create your views here.

class CreatorListView(ListView):
    model = Creator
    template_name = 'creators/creator_list.html'
    context_object_name = 'creators'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        #Search creators with username and about me information
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(about_me__icontains=search_query)
            )
        return queryset