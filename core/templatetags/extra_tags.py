from django import template
from core.models import Follow, Like, Usercomment,Friend, Team,Notification, Teaminvite,Friendrequest,Foruminappropiate
from django.contrib.auth.models import User
register = template.Library()  
# from core.models import CityList,DistrictList
# from dashboard.models import Donor,MakePayment


# @register.filter
# def social_login_citylist(self):
#     citylist = CityList.objects.all()
#     return citylist

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

@register.filter
def check_team(user_id, team_id): 
    team = Team.objects.get(id = team_id)
    if team.team_member.filter(id = user_id).exists():
        return True

@register.filter
def view_status_check(ntfc_id): 
    ntfc = Notification.objects.get(id = ntfc_id)
    if ntfc.view_status:
        return True
    else:
        return False

@register.filter
def unread_notification(user_id): 
    ntfc_number = Notification.objects.filter(user_id = user_id, view_status=False ).count()
    if ntfc_number > 0:
        return ntfc_number
    else:
        return ""

@register.filter
def team_member_check(user_id,team_id): 
    team = Team.objects.get(id = team_id)
    user = User.objects.get(id = user_id)
    tem_check = user.team_set.filter(id = team_id)
    # for user in team.team_member.all():
    if tem_check.exists():
        return True
    else:
        return False

@register.filter
def team_invite_check(user_id,team_id): 
    invite = Teaminvite.objects.filter(team_id = team_id, member_id = user_id)
    if invite.exists(): 
        return True
    else:
        return False

 

@register.filter
def friend_status(sender_id,receiver_id): 
    try:
        friend = Friend.objects.get(user_id = sender_id)
        all_friend = friend.friend_list.filter()
        flag = 0
        for frined in all_friend:
            if frined.id == receiver_id:
                flag = 1
                break
        if flag == 1:
            return True
        else:
            return False
    except:
        return False
    

@register.filter
def friend_request_status(sender_id,receiver_id): 
    request_list = Friendrequest.objects.filter(serner_id = sender_id, recever_id = receiver_id)
    if request_list.exists(): 
        for request in request_list:
            if request.status == False:
                request.delete()
                return False
            else:
                return True 
    else:
        return False

@register.filter
def friend_request_receive_status(sender_id,receiver_id): 
    user = User.objects.get(id = sender_id)
    friend = user.friend_set.filter(friend_list_id = receiver_id)  
    if friend.exists(): 
        return True
    else:
        return False


        

@register.filter
def inappropiate_post(user_id,forum_id):
    post_check =  Foruminappropiate.objects.filter(user_id = user_id, forum_id = forum_id)
    if post_check.exists():
        return True
    else:
        return False


