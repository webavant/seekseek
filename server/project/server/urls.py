from django.urls import path

from server import views

urlpatterns = [
    path('play/', views.Play.as_view()),
    path('stop/', views.Stop.as_view())
]