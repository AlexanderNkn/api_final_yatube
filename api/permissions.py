from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class IsOwnerOrReadOnly(BasePermission):
    '''
    Not allow editing/deleting post or comment if the current user is not an author
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user