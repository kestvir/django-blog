from django.urls import path
from . views import (PostListView,
                     UserPostListView,
                     PostDetailView,
                     PostDeleteView,
                     CommentDeleteView,
                     CategoryPostListView,
                     DatePostListView,
                     PostCreateView,
                     PostUpdateView)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-posts'),
    path('<str:category>/', CategoryPostListView.as_view(),
         name='blog-category-posts'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('<int:year>/<int:month>/', DatePostListView.as_view(),
         name='blog-date-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk1>/comment/<int:pk2>/delete',
         CommentDeleteView.as_view(), name='comment-delete')
]
