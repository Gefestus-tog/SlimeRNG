from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOrReadOnlyForNonSafeMethods(BasePermission):
    """
    Allows access to authenticated users for any request,
    but read-only access to unauthenticated users for non-safe methods.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated 