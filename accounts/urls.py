from django.urls import path, include
from rest_framework import routers

from .views import add_user, change_password, login, users

# router = routers.DefaultRouter()
# router.register(r'users', api_root())

urlpatterns = [
    # path('', include(router.urls)),
    path("add-user", add_user, name="add-user"),
    path("login", login, name="login"),
    path("change-password", change_password, name="login"),
    path("users", users, name="get-all-users"),
]