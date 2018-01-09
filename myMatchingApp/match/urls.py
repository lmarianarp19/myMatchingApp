from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('community/', views.community_list, name='community_list'),
    path('community/new', views.new_community, name='new_community'),
    path('new_red', views.new_red, name='new_red'),
    path('new_blue', views.new_blue, name='new_blue'),

]
