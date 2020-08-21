from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Comment, Follow, Group, Post, User
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)
from .permissions import IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly


class ApiPostViewSet(viewsets.ModelViewSet):
    '''
    List all posts, or create a new post.
    Retrieve, update or delete selected post.
    '''
    queryset = Post.objects.all().order_by("-pub_date")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ApiCommentViewSet(viewsets.ModelViewSet):
    '''
    List all comments, or create a new comment for selected post.
    Retrieve, update or delete selected comment.
    '''
    queryset = Comment.objects.all().order_by("-created")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsOwnerOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class ApiGroupViewSet(viewsets.ModelViewSet):
    '''
    List all groups, or create a new group.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ApiFollowViewSet(viewsets.ModelViewSet):
    '''
    List all followers, or subscribe to another author.
    '''
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
