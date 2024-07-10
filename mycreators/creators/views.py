from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, CreatorRequestForm, CreatorProfileForm
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
    
#Request to become creator
@login_required
def request_creator_status(request):
    if hasattr(request.user, 'creator'):
        return redirect('creator_status')
    
    if request.method == 'POST':
        form = CreatorRequestForm(request.POST)
        if form.is_valid():
            creator = form.save(commit=False)
            creator.user = request.user
            creator.status = 'PENDING'
            creator.save()
            return redirect('creator_request_submitted')
    else:
        form = CreatorRequestForm()
    return render(request, 'creators/request_creator_status.html', {'form': form})

def creator_request_submitted(request):
    return render(request, 'creators/request_creator_status_submitted.html')

@login_required
def creator_status(request):
    creator = Creator.objects.get(user=request.user)
    return render(request, 'creators/creator_status.html', {'creator': creator})

#Creator About view
class CreatorAboutMeView(DetailView):
    model = Creator
    template_name = 'creators/creator_aboutme.html'
    context_object_name = 'creator'

    def get_object(self):
        return get_object_or_404(Creator, user__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all().order_by('-created_at')
        if self.request.user.is_authenticated:
            context['is_following'] = self.object.followers.filter(id=self.request.user.id).exists()
        return context
    
#Edit Creator About view
class EditCreatorAboutMeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Creator
    form_class = CreatorProfileForm
    template_name = 'creators/edit_creator_aboutme.html'

    def get_object(self):
        return self.request.user.creator

    def test_func(self):
        creator = self.get_object()
        return self.request.user == creator.user

    def get_success_url(self):
        return reverse_lazy('creator_aboutme', kwargs={'username': self.request.user.username})

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

#View post
class PostDetailView(DetailView):
    model = Post
    template_name = 'creators/post_detail.html'
    context_object_name = 'post'

# Add Comments
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post.add_comment(request.user, content)
    return redirect('post_detail', pk=post_id)
# DeleteComments
@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = next((c for c in post.comments if c['id'] == comment_id), None)
    if comment and comment['user_id'] == request.user.id:
        post.delete_comment(comment_id)
    return redirect('post_detail', pk=post_id)