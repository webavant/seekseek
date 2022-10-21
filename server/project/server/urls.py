from django.urls import path

from server import views

urlpatterns = [
    path('play/', views.Play.as_view()),
    path('pause/', views.Pause.as_view()),
    path('stop/', views.Stop.as_view()),
    path('status/', views.Status.as_view()),
    path('search/', views.Search.as_view()),
    path('episodes/', views.Episodes.as_view()),
]