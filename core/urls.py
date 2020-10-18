from django.urls import path
app_name = 'core'
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('follow-community/', views.follow_community, name='follow_community'),
    path('community/following', views.community_following, name='community_following'),
    path('community/details/<int:id>/', views.community_details, name='community_details'),
    path('add-community-content/<int:id>/', views.add_communitycontent, name='add_communitycontent'),
    path('publish-content/<int:cid>/<str:image>/<str:content>', views.publish_communitycontent, name='publish_communitycontent'),
    path('add-like', views.add_like, name='add_like'),
    path('add-usercomment/<int:forum_id>', views.add_usercomment, name='add_usercomment'),
    path('edit-usercomment/<int:id>', views.comment_edit, name='comment_edit'),
    path('delete-comment/<int:id>', views.comment_delete, name='comment_delete'),
    path('api/get_places/', views.get_places, name='get_places'),





    path('<str:name>/', views.property, name='property'),

]
