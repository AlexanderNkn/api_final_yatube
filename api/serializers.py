from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Post, Comment, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    group = serializers.SlugRelatedField(
        slug_field='title', queryset=Group.objects.all(), required=False,
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )
    user = serializers.ReadOnlyField(source='user.username')

    def validate_following(self, value):
        '''
        Check if request.user already followed by author
        '''
        if Follow.objects.filter(user=self.context['request'].user, following=value).exists():
            raise ValidationError('You are already followed by author')
        return value

    class Meta:
        model = Follow
        fields = '__all__'
