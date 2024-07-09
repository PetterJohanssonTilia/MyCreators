from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Creator, Post


# Create your views here.

#=============== List of creators ===============
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

#=============== Creators about me page =================
class CreatorAboutMeView(DetailView):
    model = Creator
    template_name = 'creators/creator_aboutme.html'
    context_object_name = 'creator'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().order_by('-created_at')
        return context
    
@login_required
def follow_creator(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    creator.followers.add(request.user)
    return redirect('creator_aboutme', pk=pk)

@login_required
def unfollow_creator(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    creator.followers.remove(request.user)
    return redirect('creator_aboutme', pk=pk)

class FollowedCreatorsView(LoginRequiredMixin, ListView):
    template_name = 'creators/followed_creators.html'
    context_object_name = 'followed_creators'

    def get_queryset(self):
        return Creator.objects.filter(followers=self.request.user)

class PersonalizedFeedView(LoginRequiredMixin, ListView):
    template_name = 'creators/personalized_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        followed_creators = Creator.objects.filter(followers=self.request.user)
        return Post.objects.filter(creator__in=followed_creators).order_by('-created_at')