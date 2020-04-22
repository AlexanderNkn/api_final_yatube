from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'^posts', views.ApiPostViewSet)
router.register(r'^posts/(?P<post_id>\d+)/comments', views.ApiCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
