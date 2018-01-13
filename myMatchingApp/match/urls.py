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
    path('communityit/<int:pk>/delete/', views.CommunityDelete.as_view(), name='community_delete'),
    path('community/<int:pk>/', views.community_details, name='community_details'),
    path('community/<int:pk>/', views.community_details, name='community_details'),
    path('blue/<int:pk>/', views.blue_details, name='blue_details'),
    path('red/<int:pk>/', views.red_details, name='red_details'),
    path('new_ranking_blue/<int:blue_id>/<int:red_id>/', views.new_ranking_blue, name='new_ranking_blue'),
    path('new_ranking_red/<int:red_id>/<int:blue_id>/', views.new_ranking_red, name='new_ranking_red'),
    path('ranking_list/', views.ranking_list, name='ranking_list'),
    path('new_matching/', views.new_matching, name='new_matching'),
    # path('matching/create/', views.MatchingCreate.as_view(), name='matching_create'),
    # path('matching/<int:pk>/update/', views.MatchingUpdate.as_view(), name='matching_update'),
    # path('matching/<int:pk>/delete/', views.MatchingDelete.as_view(), name='matching_delete'),

]
