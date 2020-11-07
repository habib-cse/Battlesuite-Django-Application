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

# Register your models here.
admin.site.register(Community)
admin.site.register(Follow)
admin.site.register(Communityforum)
admin.site.register(Like)
admin.site.register(Usercomment)
admin.site.register(Hashtag) 
admin.site.register(Friend) 
admin.site.register(Notification) 
admin.site.register(Team)  
admin.site.register(Teaminvite)  
admin.site.register(Friendrequest)  
admin.site.register(Foruminappropiate)  
 