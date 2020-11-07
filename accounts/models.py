from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Mainuser(models.Model):
    TAG = (
        ('xbox','xbox'),
        ('playstation','playstation'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='uploads/user/', blank=True, null = True)
    bgimage = models.ImageField(upload_to='uploads/user/', blank=True, null = True)
    pro_status = models.BooleanField(default=False)
    pro_signup_type = models.CharField(choices=TAG, max_length=50, blank=True, null=True)
    status = models.BooleanField(default=False)
    
    

    class Meta:
        verbose_name = "Mainuser"
        verbose_name_plural = "Mainusers"

    def __str__(self):
        return "{}".format(self.user.username)