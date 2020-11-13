from django.db import models
# Create your models here.
from django.contrib.auth.models import User


def team_based_upload_to(instance, filename):
    return "uploads/teams/{}.png".format(instance.name)

class TestConnection(models.Model):
    pass

class Team(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    icon = models.ImageField(upload_to=team_based_upload_to)
    
    def __str__(self):
        return self.name 
        
class TeamUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.team) + " - " + str(self.user)

class Tournament(models.Model):
    name = models.CharField(max_length=250)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=250)
    date = models.DateTimeField()
    game_length = models.IntegerField() # minutes
    description = models.TextField()
    platform = models.CharField(max_length=250)
    player_amount = models.IntegerField()
    number_of_teams = models.IntegerField()
    def __str__(self):
        return self.name

class Game(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    players = models.ManyToManyField(User)
    duration = models.IntegerField() # minutes

class TournamentRound(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)

class LoadingScreen(models.Model):
    Game = models.OneToOneField(Game, on_delete=models.CASCADE, unique=True)
    players = models.ManyToManyField(User)

class LoadingScreenAdmin(models.Model):
    loadingscreen = models.OneToOneField(LoadingScreen, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    ready = models.BooleanField(default=False)

class LoadingScreenReadyPlayers(models.Model):
    loadingscreen = models.OneToOneField(LoadingScreen, on_delete=models.CASCADE)
    players = models.ManyToManyField(User)
    

class GameTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

class Challenge(models.Model):
    host_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="+")
    challenged_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ["tournament", "host_team", "challenged_team"]

class TournamentInvite(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["tournament", "user"]
    
class TournamentTeam(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tournament.name + " - " + self.team.name
    class Meta:
        unique_together = ["tournament", "team"]


class TournamentTeamUser(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["tournament", "team", "user"]

class Community(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='uploads/community/')
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Community"
        verbose_name_plural = "Communitys"

    def __str__(self):
        return self.name 


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    following_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Follows"

    def __str__(self):
        return "{} -- {}".format(self.user.username, self.community.name)

class Communityforum(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/comment/')
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True) 

    class Meta:
        verbose_name = "Community Forum"
        verbose_name_plural = "Community Forum"

    def __str__(self):
        return "{} -- {}".format(self.user.username, self.community)



class Like(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    communityforum = models.ForeignKey(Communityforum, on_delete=models.CASCADE) 
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)  

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return "{}".format(self.user.username)

class Usercomment(models.Model):
    commented_user = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_forum = models.ForeignKey(Communityforum, on_delete=models.CASCADE)
    comment_text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "User Comment"
        verbose_name_plural = "User Comments"

    def __str__(self):
        return "{}".format(self.commented_user.username)


class Agency(models.Model):
    name = models.CharField(max_length=299)
    address = models.TextField()
    domain_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "agency"
        verbose_name_plural = "agencys"

    def __str__(self):
        return self.name 

class Property(models.Model):
    name = models.CharField(max_length=200)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/agency/') 
    

    class Meta:
        verbose_name = "Property" 
        verbose_name_plural = "Propertys"

    def __str__(self):
        return self.name 
