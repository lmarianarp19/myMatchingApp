from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('community/', views.community_list, name='community_list'),
    # path('community/new', views.new_community, name='new_community'),
    path('new_red', views.new_red, name='new_red'),
    path('new_blue', views.new_blue, name='new_blue'),
    path('community/create/', views.CommunityCreate.as_view(), name='community_create'),
    path('community/<int:pk>/update/', views.CommunityUpdate.as_view(), name='community_update'),
    path('commit/<int:pk>/delete/', views.CommunityDelete.as_view(), name='community_delete'),
    path('commit/<int:pk>/', views.community_details, name='community_details'),

]
