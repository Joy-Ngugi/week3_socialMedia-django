from django.urls import path
# from .views import  ProfileListCreateView, PostDetailView, CommentDetailView, FollowDetailView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
 # path('', views.helloWorld, name='hello'),
 path('', views.home, name='home'),
 path('accounts/register/', views.register, name='register'),
 path('accounts/password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
 path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
 path('accounts/reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
 path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
 path('api/profile/<int:pk>/', views.ProfileDetailView.as_view(), name='book-list-create'),
 path('api/posts/', views.PostListView.as_view(), name='book-detail'),
 path('api/posts/<int:pk>/', views.PostDetailView.as_view(), name='book-detail'),
 path('api/posts/<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
 path('api/comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
 path('api/posts/<int:post_id>/like/', views.PostLike.as_view(), name='post-like'),
 path('api/comments/<int:comment_id>/like/', views.CommentLike.as_view(), name='comment-like'),
 path('api/posts/<int:post_id>/like/', views.PostUnlike.as_view(), name='post-unlike'),
 path('api/comments/<int:comment_id>/like/', views.CommentUnlike.as_view(), name='comment-unlike'),
 path('api/users/<int:user_id>/follow/', views.UserFollow.as_view(), name='user-follow'),
 path('api/users/<int:user_id>/follow/', views.UserUnfollow.as_view(), name='user-unfollow'),
 path('api/search/users/', views.UserSearch.as_view(), name='user-search'),
 path('api/posts/create/', views.PostCreateView.as_view(), name='create_post'),
 path('profile/', views.profile, name='profile'),
 path('profile/update/', views.profile_update, name='profile_update'),
 path('post/create_post/', views.create_post, name='create_post'),
 path('post/<int:post_id>/', views.post_detail, name='post_detail'),
 path('post/<int:post_id>/like/', views.like_post, name='like_post'),
 path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
 path('follow/<str:username>/', views.follow_user, name='follow_user'),
 path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
 path('profile/<str:username>/', views.profile_view, name='profile'),
 path('profile/other/<str:username>/', views.other_profile_view, name='other_profile_view'),
 path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
 path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
 ]