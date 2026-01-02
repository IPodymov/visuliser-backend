from django.urls import path
from .views import RegisterView, LoginView, LogoutView, SetCSRFCookieView, UserMeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("set-csrf/", SetCSRFCookieView.as_view(), name="set-csrf"),
    path("me/", UserMeView.as_view(), name="user-me"),
]
