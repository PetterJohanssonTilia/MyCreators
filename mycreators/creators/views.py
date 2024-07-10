from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from .forms import UserRegisterForm
from .models import Creator, Post


# Create your views here.

#Index
class IndexView(TemplateView):
    template_name = 'creators/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creators'] = Creator.objects.all()
        return context

#All creators
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
    
#Creator about me
class CreatorAboutMeView(DetailView):
    model = Creator
    template_name = 'creators/creator_aboutme.html'
    context_object_name = 'creator'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().order_by('-created_at')
        if self.request.user.is_authenticated:
            context['is_following'] = self.object.followers.filter(id=self.request.user.id).exists()
        return context

#Follow creator
@login_required
def follow_creator(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    creator.followers.add(request.user)
    return redirect('creator_aboutme', pk=pk)

#Unfollow creator
@login_required
def unfollow_creator(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    creator.followers.remove(request.user)
    return redirect('creator_aboutme', pk=pk)

#Followed creators
class FollowedCreatorsView(LoginRequiredMixin, ListView):
    template_name = 'creators/creator_followed.html'
    context_object_name = 'followed_creators'

    def get_queryset(self):
        return Creator.objects.filter(followers=self.request.user)
    
#Feed
class PersonalizedFeedView(LoginRequiredMixin, ListView):
    template_name = 'creators/personalized_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        followed_creators = Creator.objects.filter(followers=self.request.user)
        return Post.objects.filter(creator__in=followed_creators).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

#Register
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})