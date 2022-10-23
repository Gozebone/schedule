from django.urls import path
from apps.function_caller import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_events/', views.create_events, name='create_events'),
]
