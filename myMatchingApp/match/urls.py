from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('community/', views.community_list, name='community_list'),
    # path('community/new', views.new_community, name='new_community'),
    path('new_red', views.new_red, name='new_red'),
    path('new_blue', views.new_blue, name='new_blue'),
    # path('community/new/', views.community_new, name='community_new'),
    # path('community/<int:pk>/edit/', views.community_edit, name='community_edit'),
    path('community/<int:pk>/delete/', views.CommunityDelete.as_view(), name='community_delete'),
    path('community/<int:pk>/', views.community_details, name='community_details'),
    path('blue/<int:pk>/', views.blue_details, name='blue_details'),
    path('red/<int:pk>/', views.red_details, name='red_details'),
    path('new_ranking_by_blue/<int:blue_id>/<int:red_id>/', views.new_ranking_by_blue, name='new_ranking_by_blue'),
    path('new_ranking_by_red/<int:red_id>/<int:blue_id>/', views.new_ranking_by_red, name='new_ranking_by_red'),
    path('ranking_list/', views.ranking_list, name='ranking_list'),
    path('new_matching/', views.New_matching.as_view(), name='new_matching'),
    path('matching_list/', views.matching_list, name='matching_list'),
    path('pairing_list/', views.pairing_list, name='pairing_list'),
    path('match/<int:pk>/', views.matching_details, name='matching_details'),
    path('community/new/', views.CommunityCreate.as_view(), name='community_new'),
    path('commmunity/<int:pk>/edit/', views.CommunityUpdate.as_view(), name='community_edit'),
    path('matching/<int:pk>/delete/', views.MatchingDelete.as_view(), name='matching_delete'),
    # path('matching/<int:pk>/delete/', views.MatchingDelete.as_view(), name='matching_delete'),

]
