from django.contrib import admin
from .models import (
    Community,
    Follow,
    Communityforum,
    Like,
    Usercomment, 
    Hashtag,
    Friend,
    Notification,
    Team,
    Teaminvite,
    Friendrequest,
    Foruminappropiate,
)
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(Community)
class CommunityAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Community

@admin.register(Communityforum)
class CommunityforumAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Communityforum
 

@admin.register(Follow)
class FollowAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Follow
 

@admin.register(Like)
class LikeAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Like
 

@admin.register(Usercomment)
class UsercommentAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Usercomment
 

@admin.register(Hashtag)
class HashtagAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Hashtag
 

@admin.register(Friend)
class FriendAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Friend
 

@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Notification
 

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Team
 

@admin.register(Teaminvite)
class TeaminviteAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Teaminvite
 

@admin.register(Friendrequest)
class FriendrequestAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Friendrequest
 

@admin.register(Foruminappropiate)
class ForuminappropiateAdmin(ImportExportModelAdmin):
    
    class Meta:
        model = Foruminappropiate
 
