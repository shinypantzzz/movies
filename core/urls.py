from django.urls import path

from . import views
from .routers import Router

router = Router()

router.register('movies', views.MovieViewSet, basename="movie")
router.register('users', views.UserViewSet, basename="user")

urlpatterns = [
    *router.urls,
    path('register/', views.RegisterView.as_view(), name="register")
]