from django.urls import path
app_name = 'core'
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('follow-community/', views.follow_community, name='follow_community'),
    path('community/following', views.community_following, name='community_following'),
    path('community/details/<int:id>/', views.community_details, name='community_details'),
    path('inappropiate-post/<int:forum_id>/<int:community_id>', views.create_inappropiate_post, name='create_inappropiate_post'),
    path('add-community-content/<int:id>/', views.add_communitycontent, name='add_communitycontent'),
    path('publish-content/<int:cid>/<str:image>/<str:content>', views.publish_communitycontent, name='publish_communitycontent'),
    path('add-like', views.add_like, name='add_like'),
    path('add-usercomment/<int:forum_id>', views.add_usercomment, name='add_usercomment'),
    path('edit-usercomment/<int:id>', views.comment_edit, name='comment_edit'),
    path('delete-comment/<int:id>', views.comment_delete, name='comment_delete'),
    path('api/get_places/', views.get_places, name='get_places'),
    path('team-default', views.team_default, name='team_default'),
    path('create-team', views.create_team, name='create_team'),
    path('team-details/<int:id>', views.team_details, name='team_details'),
    path('team-update/<int:id>', views.team_update, name='team_update'),
    path('joining-team-request/<int:team_id>/<int:team_admin_id>', views.joining_team_request, name='joining_team_request'),
    path('invaitation-accept/<int:team_id>/<int:invite_id>', views.invaitation_accept, name='invaitation_accept'),
    path('invaitation-decline/<int:team_id>/<int:invite_id>', views.invaitation_decline, name='invaitation_decline'),
    path('notification', views.notification_list, name='notification_list'),
    path('notification-details/<int:id>', views.notification_details, name='notification_details'),
    path('search-team-player', views.search_team_player, name='search_team_player'),
    path('player-profile/<int:id>', views.player_profile, name='player_profile'),
    path('player-profile-update/', views.player_profile_update, name='player_profile_update'),
    path('send-friend-request/<int:recever_id>', views.send_friend_request, name='send_friend_request'),
    path('cancel-friend-request/<int:recever_id>', views.friend_request_cancel, name='friend_request_cancel'),
    path('friend-request-accept/<int:sender_id>/<int:request_id>', views.friend_request_accept, name='friend_request_accept'),
    path('friend-request-decline/<int:sender_id>/<int:request_id>', views.friend_request_decline, name='friend_request_decline'),



 

]
