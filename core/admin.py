from django.contrib import admin
from .models import (
    Community,
    Follow,
    Communityforum,
    Like,
    Usercomment,
    Agency,
    Property,
    Team,
    TeamUser,
    Game,
    Challenge,
    Tournament
)

# Register your models here.
admin.site.register(Community)
admin.site.register(Follow)
admin.site.register(Communityforum)
admin.site.register(Like)
admin.site.register(Usercomment)
admin.site.register(Agency)
admin.site.register(Property) 
admin.site.register(Team)
admin.site.register(TeamUser) 
admin.site.register(Game)
admin.site.register(Challenge)
admin.site.register(Tournament) 