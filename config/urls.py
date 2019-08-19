from django.urls import path

from tickets import views

urlpatterns = [
    path('', views.home, name='home')
]
