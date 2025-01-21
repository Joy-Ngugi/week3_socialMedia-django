from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import Profile, Post, Comment, Like, Dislike, Follow
from .serializers import PostSerializer, ProfileSerializer, CommentSerializer
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileUpdateForm, UserUpdateForm, PostForm, CommentForm
import cloudinary.uploader
from django.db import IntegrityError

@login_required

def home(request):
    all_posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': all_posts})

def error_404(request, exception):
  return render(request, '404.html')

def register(request):
 if request.method == 'POST':
   form = RegistrationForm(request.POST)
   if form.is_valid():
     form.save()
     return redirect('login')
 else:
   form = RegistrationForm()
 return render(request, 'registration/register.html', {'form': form})

class ProfileDetailView(generics.RetrieveUpdateAPIView):
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer
  
class PostCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
class PostListView(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  
class CommentListCreateView(generics.ListCreateAPIView):
  # queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  
  def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

  def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(post_id=post_id, author=self.request.user)
  
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostLike(APIView):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        Like.objects.create(user=request.user, post=post)
        return Response(status=status.HTTP_201_CREATED)

class CommentLike(APIView):
    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        Like.objects.create(user=request.user, comment=comment)
        return Response(status=status.HTTP_201_CREATED)

class PostUnlike(APIView):
    def delete(self, request, post_id):
        Like.objects.filter(user=request.user, post_id=post_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentUnlike(APIView):
    def delete(self, request, comment_id):
        Like.objects.filter(user=request.user, comment_id=comment_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserFollow(APIView):
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        request.user.profile.following.add(user)
        return Response(status=status.HTTP_201_CREATED)

class UserUnfollow(APIView):
    def delete(self, request, user_id):
        user = User.objects.get(id=user_id)
        request.user.profile.following.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserSearch(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return Profile.objects.filter(user__username__icontains=query)

@login_required
def profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)
        return redirect('profile_update')

    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    followers_count = Follow.objects.filter(followed=request.user).count()
    following_count = Follow.objects.filter(follower=request.user).count()

    
    is_following = Follow.objects.filter(follower=request.user, followed=user_profile.user).exists()

    print(f"Is following: {is_following}")  

    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'user_posts': user_posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,  
    })
    

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username) 
    posts = Post.objects.filter(author=user)  
    followers = Follow.objects.filter(followed=user)  
    following = Follow.objects.filter(follower=user)
    
    posts_with_comments = posts.prefetch_related('comments')
    
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()

    context = {
        'user': user,
        'posts': posts_with_comments,
        'followers': followers,
        'following': following,
        'is_following': is_following,
    }
    return render(request, 'profile.html', context)

def other_profile_view(request, username):
    user = get_object_or_404(User, username=username)  
    posts = Post.objects.filter(author=user) 
    followers = Follow.objects.filter(followed=user)  
    following = Follow.objects.filter(follower=user)  
    is_following = Follow.objects.filter(follower=request.user, followed=user).exists()
    followers_count = Follow.objects.filter(followed=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    
    context = {
        'user': user,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'other_profile.html', context)

@login_required
def profile_update(request):
    user_profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile',  username=request.user.username) 
    else:
        profile_form = ProfileUpdateForm(instance=user_profile, user=request.user)

    return render(request, 'profile_update.html', {'profile_form': profile_form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
   
    if post.author == request.user:
        post.delete()  
    return redirect('profile', username=request.user.username)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            
            
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})



def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    user_liked = post.likes.filter(user=request.user).exists()
    user_disliked = post.dislikes.filter(user=request.user).exists()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'user_disliked': user_disliked
    })
    
    
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post.likes.filter(user=request.user).exists():
        Like.objects.create(post=post, user=request.user)
        post.dislikes.filter(user=request.user).delete()  
    return redirect('post_detail', post_id=post_id)

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post.dislikes.filter(user=request.user).exists():
        Dislike.objects.create(post=post, user=request.user)
        post.likes.filter(user=request.user).delete()  
    return redirect('post_detail', post_id=post_id)



def follow_user(request, username):
   
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user != user_to_follow:  
        
        if not Follow.objects.filter(follower=request.user, followed=user_to_follow).exists():
            try:
                Follow.objects.create(follower=request.user, followed=user_to_follow)
            except IntegrityError:
                
                pass
    
    
    return redirect('other_profile_view', username=username)

def unfollow_user(request, username):
    
    user_to_unfollow = get_object_or_404(User, username=username)
    
    if request.user != user_to_unfollow:  
        
        Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    
    
    return redirect('other_profile_view', username=username)


def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')

        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
        
        return redirect('profile', username=request.user.username)
