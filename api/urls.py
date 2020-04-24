from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views


router = DefaultRouter()
router.register(r'posts', views.ApiPostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', views.ApiCommentViewSet)
router.register(r'group', views.ApiGroupViewSet)
router.register(r'follow', views.ApiFollowViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
