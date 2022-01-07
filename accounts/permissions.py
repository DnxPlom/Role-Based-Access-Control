
from rest_framework.response import Response


class AdminRole:
    def has_permission(self, request, view):
        if request.user.usermodel.role != "admin":
            return False
        return bool(request.user and request.user.is_authenticated)
