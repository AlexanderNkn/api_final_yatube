from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Comment, Follow, Group, Post, User
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class ApiPostViewSet(viewsets.ModelViewSet):
    '''
    List all posts, or create a new post.
    Retrieve, update or delete selected post.
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

#    Предыдущий рабочий вариант, оставил на память
#    def get_queryset(self):
#        queryset = Post.objects.all()
#        # get group from GET-request, if group exists
#        group = self.request.query_params.get('group', None)
#        if group is not None:
#            queryset = get_list_or_404(queryset, group=group)
#        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        if post.author != self.request.user:
            raise PermissionDenied
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied
        instance.delete()


class ApiCommentViewSet(viewsets.ModelViewSet):
    '''
    List all comments, or create a new comment for selected post.
    Retrieve, update or delete selected comment.
    '''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments
    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        comment = Comment.objects.get(pk=self.kwargs.get('pk'))
        if comment.author != self.request.user:
            raise PermissionDenied
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied
        instance.delete()


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

#    Предыдущий рабочий вариант, оставил на память
#    def get_queryset(self):
#        queryset = Follow.objects.all()
#        # get 'username' from GET-request, if 'search' exists
#        username = self.request.query_params.get('search', None)
#        if username is not None:
#            queryset1 = queryset.filter(user__username=username)
#            queryset2 = queryset.filter(following__username=username)
#            queryset = queryset1 | queryset2
#        return queryset 

    def perform_create(self, serializer):
        # check if request.user already followed by author
        new_following_username = self.request.data.get('following', None)
        new_following = User.objects.get(username=new_following_username)
        already_following = Follow.objects.filter(user=self.request.user)
        already_following_list = [item.following for item in already_following]
        if new_following in already_following_list:
            raise ValidationError('You are already followed by author')
        serializer.save(user=self.request.user)
