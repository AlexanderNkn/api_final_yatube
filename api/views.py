from django.core.exceptions import PermissionDenied
from rest_framework import viewsets

from .models import Comment, Post, Group
from .serializers import CommentSerializer, PostSerializer, GroupSerializer


class ApiPostViewSet(viewsets.ModelViewSet):
    '''
    List all posts, or create a new post.
    Retrieve, update or delete selected post.
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        #  получаем параметр group из GET-запроса, если group передан
        group = self.request.query_params.get('group', None)
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset

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
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__id=post_id)

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