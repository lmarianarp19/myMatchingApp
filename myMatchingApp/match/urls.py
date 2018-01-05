from django.urls import path

from . import views

urlpatterns = [
    path('community/', views.community_list, name='community_list'),
]
