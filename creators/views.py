from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import UserRegisterForm, CreatorRequestForm, CreatorProfileForm, PostForm
from .models import Creator, Post

#================= Index =================

#Index
class IndexView(TemplateView):
    template_name = 'creators/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creators'] = Creator.objects.all()
        return context

#================= Creators =================

#All creators
class CreatorListView(ListView):
    model = Creator
    template_name = 'creators/creator_list.html'
    context_object_name = 'creators'
    
    #Search creators
    def get_queryset(self):
        queryset = super().get_queryset().filter(status='APPROVED')
        search_query = self.request.GET.get('search')
        #Search creators with username and about me information
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(about_me__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['followed_creators'] = Creator.objects.filter(followers=self.request.user)
        context['creator_types'] = dict(Creator.CREATOR_TYPES)
        
        if self.request.user.is_staff or self.request.user.is_superuser:
            context['pending_creators'] = Creator.objects.filter(
                Q(status__iexact='PENDING') & Q(about_me='')
            )
        
        return context
    
#Request to become creator
@login_required
def request_creator_status(request):
    if hasattr(request.user, 'creator'):
        return redirect('creator_status')
    
    if request.method == 'POST':
        form = CreatorRequestForm(request.POST)
        if form.is_valid():
            creator_type = form.cleaned_data['creator_type']
            request_message = form.cleaned_data['request_message']
            
            Creator.objects.create(
                user=request.user,
                creator_type=creator_type,
                request_message=request_message,
                status='PENDING'
            )

            return redirect('creator_request_submitted')
    else:
        form = CreatorRequestForm()
    return render(request, 'creators/request_creator_status.html', {'form': form})

def creator_request_submitted(request):
    return render(request, 'creators/request_creator_status_submitted.html')

@login_required
def creator_status(request):
    creator = Creator.objects.get(user=request.user)
    return render(request, 'creators/creator_status.html', {
        'creator': creator,
        })

# Admin - Accept/Reject creators
def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_or_superuser)
def approve_creator(_request, username):
    creator = get_object_or_404(Creator, user__username=username, status='PENDING')
    creator.status = 'APPROVED'
    creator.save()
    return redirect('creator_list')

@login_required
@user_passes_test(is_staff_or_superuser)
def reject_creator(_request, username):
    creator = get_object_or_404(Creator, user__username=username, status='PENDING')
    creator.status = 'REJECTED'
    creator.save()
    return redirect('creator_list')
    
#================= Sign up / Delete =================

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

#Delete Creator Account   
class DeleteCreatorAccount(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Creator
    template_name = 'creators/delete_account_confirm.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user.creator

    def test_func(self):
        return hasattr(self.request.user, 'creator')

    def delete(self, request, *args, **kwargs):
        user = self.get_object().user
        response = super().delete(request, *args, **kwargs)
        user.delete()
        logout(request)
        return response
    
#================= Personal page =================   

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
    

#================= Follow/Unfollow =================

#Follow creator
@login_required
def follow_creator(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    creator.followers.add(request.user)
    return redirect('creator_aboutme', username=creator.user.username)

#Unfollow creator
@login_required
def unfollow_creator(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    creator.followers.remove(request.user)
    return redirect('creator_aboutme', username=creator.user.username)

#Followed creators - list
class FollowedCreatorsView(LoginRequiredMixin, ListView):
    template_name = 'creators/creator_followed.html'
    context_object_name = 'followed_creators'

    def get_queryset(self):
        return Creator.objects.filter(followers=self.request.user)

#================= Feed =================
    
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

#View post
class PostDetailView(DetailView):
    model = Post
    template_name = 'creators/post_detail.html'
    context_object_name = 'post'

#Add Comments
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post.add_comment(request.user, content)
    return redirect('post_detail', pk=post_id)

#DeleteComments
@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = next((c for c in post.comments if c['id'] == comment_id), None)
    if comment and comment['user_id'] == request.user.id:
        post.delete_comment(comment_id)
    return redirect('post_detail', pk=post_id)

#================= Create Posts =================

#Create Post
class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'creators/create_post.html'
    success_url = reverse_lazy('creator_aboutme')

    def form_valid(self, form):
        form.instance.creator = self.request.user.creator
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('creator_aboutme', kwargs={'username': self.request.user.username})

#Edit Post
class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'creators/edit_post.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user.creator == post.creator

    def get_success_url(self):
        return reverse_lazy('creator_aboutme', kwargs={'username': self.request.user.username})

#Delete Post
class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'creators/delete_post_confirm.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user.creator == post.creator

    def get_success_url(self):
        return reverse_lazy('creator_aboutme', kwargs={'username': self.request.user.username})