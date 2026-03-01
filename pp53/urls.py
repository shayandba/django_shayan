from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exercici1/', views.exercici1, name='exercici1'),
    path('exercici2/', views.exercici2, name='exercici2'),
    path('exercici3/', views.exercici3, name='exercici3'),
]
