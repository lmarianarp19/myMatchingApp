from django.urls import path

from . import views

urlpatterns = [
    path('community/', views.community_list, name='community_list'),
    path('community/new', views.new_community, name='new_community'),
]
