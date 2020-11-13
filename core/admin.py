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
    Tournament,
    TournamentInvite,
    TournamentTeam,
    TournamentTeamUser,
    GameTeam,
    LoadingScreen,
    TournamentRound,
    LoadingScreenAdmin
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
admin.site.register(TournamentInvite) 
admin.site.register(TournamentTeam) 
admin.site.register(TournamentTeamUser)
admin.site.register(GameTeam)
admin.site.register(LoadingScreen)
admin.site.register(TournamentRound)
admin.site.register(LoadingScreenAdmin)