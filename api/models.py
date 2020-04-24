from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    '''Модель групп пользователей'''
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    '''Модель постов пользователей'''
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True,)

    def __str__(self):
        return self.text


class Comment(models.Model):
    '''Модель постов пользователей'''
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField('Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    '''Модель подписки на авторов'''
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    class Meta:
        unique_together = ('following', 'user')