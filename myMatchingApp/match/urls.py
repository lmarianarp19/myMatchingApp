from django.urls import path

from . import views

urlpatterns = [
    path('community/', views.community_list, name='community_list'),
    path('community/new', views.new_community, name='new_community'),
    path('community/<id>/new_woman', views.new_woman, name='new_woman'),
    path('community/<id>/new_man', views.new_man, name='new_man'),

]
