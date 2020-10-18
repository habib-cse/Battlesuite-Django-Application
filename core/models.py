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
