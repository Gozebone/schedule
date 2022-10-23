from django.urls import path
import apps.functionCaller.views

urlpatterns = [
    path('', apps.functionCaller.views.index, name='index'),
    path('create_events/', apps.functionCaller.views.create_events, name='create_events'),
]
