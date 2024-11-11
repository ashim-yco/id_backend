from django.urls import path
from authentication.api import user_view

urlpatterns = [
    path("registeruser/", user_view.UserRegisterView.as_view(), name="RegisterUser"),
    path("loginuser/", user_view.UserLoginView.as_view(), name="LoginUser"),
    path("getallusers/", user_view.AllUsersView.as_view(), name="GetAllUsers"),
]
