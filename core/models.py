from django.db import models
# Create your models here.
from django.contrib.auth.models import User

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

class Foruminappropiate(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    forum = models.ForeignKey(Communityforum, on_delete=models.CASCADE) 
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True) 

    class Meta:
        verbose_name = "Inappropriate Forum"
        verbose_name_plural = "Inappropriate Forums"

    def __str__(self):
        return "{} -- {}".format(self.user.username)




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

class Hashtag(models.Model):
    tag = models.CharField(max_length=100)
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default = True) 

    class Meta:
        verbose_name = "Hashtag"
        verbose_name_plural = "Hashtags"

    def __str__(self):
        return self.tag   


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete =models.CASCADE, related_name="main_user")
    friend_list = models.ManyToManyField(User)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False) 

    class Meta:
        verbose_name = "Friend"
        verbose_name_plural = "Friends"

    def __str__(self):
        return "{}".format(self.user.username)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    view_status = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return "{} - {}".format(self.title , self.user.username)


class Team(models.Model):
    name = models.CharField(max_length=150)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_admin")
    logo = models.ImageField(upload_to='uploads/team')
    background_image = models.ImageField(upload_to='uploads/team')
    team_member = models.ManyToManyField(User)
    datetime = models.DateTimeField(auto_now_add=True)
    hastag = models.ManyToManyField(Hashtag)
    status = models.BooleanField(default=True) 

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name 
 
class Teaminvite(models.Model): 
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    receive_status = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    class Meta:  
        verbose_name = 'Teaminvite'
        verbose_name_plural = 'Teaminvites'

    def __str__(self):
        return "{}".format(self.team)

class Friendrequest(models.Model):
    serner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recever = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    accepted_status = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    class Meta:  
        verbose_name = 'Friend Request'
        verbose_name_plural = 'Friend Requests'

    def __str__(self):
        return "{} {}".format(self.serner, self.recever)