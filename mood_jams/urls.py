from django.urls import path
from recommender import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detect/', views.detect_emotion, name='detect_emotion'),
]