from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size = 5


class CustomUpdatePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False
