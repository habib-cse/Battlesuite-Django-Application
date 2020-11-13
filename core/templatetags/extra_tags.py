from django import template
from core.models import Follow, Like, Usercomment
register = template.Library()  
# from core.models import CityList,DistrictList
# from dashboard.models import Donor,MakePayment


# @register.filter
# def social_login_citylist(self):
#     citylist = CityList.objects.all()
#     return citylist

def media():
    return "media/uploads"

@register.filter
def following_check(user_id, community_id): 
    following_check = Follow.objects.filter(user_id = user_id, community_id = community_id)
    if following_check.exists():
        return True
    else:
        return False

@register.filter
def liked(user_id, coment_id): 
    like_check = Like.objects.filter(user_id = user_id, communityforum = coment_id)
    if like_check.exists():
        return True
    else:
        return False

@register.filter
def total_number_of_like(coment_id): 
    number_of_like = Like.objects.filter(communityforum_id = coment_id).count()
    return number_of_like

@register.filter
def comment_count(coment_id): 
    number_of_comments = Usercomment.objects.filter(commented_forum_id = coment_id).count()
    

    
    return number_of_comments
