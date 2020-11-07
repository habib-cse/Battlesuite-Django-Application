from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from accounts.models import Mainuser
from .models import Community, Follow, Communityforum, Like,Friendrequest, Usercomment,Hashtag, Friend, Notification, Team,Teaminvite,Foruminappropiate
from django.contrib.auth.decorators import login_required
from django.core.files.storage import  FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    return render(request,'frontend/index.html'
    )
@login_required()
def follow_community(request):
    community_list = Community.objects.filter(status=True).order_by('name')
    search = ""
    if request.method == 'POST':
        search = request.POST.get('search')
        community_list = community_list.filter(name__icontains = search)
     
    page = request.GET.get('page',1)
    paginator = Paginator(community_list, 15)
    try:
        community_lists = paginator.page(page)
    except PageNotAnInteger:
        community_lists = paginator.page(1)
    except EmptyPage:
        community_lists = paginator.page(paginator.num_pages)

    context = {
        'community_list':community_lists,
        'search':search,
    }
    return render(request, 'frontend/follow_community.html',context)
    
@login_required
def community_following(request):
    if request.is_ajax():
        community_id = int(request.GET.get('community_id'))
        user_id = request.user.id
        Follow.objects.create(user_id = user_id, community_id = community_id)
        return JsonResponse({"message":"Following"})
        
@login_required
def community_details(request, id):
    community = Community.objects.get(id = id)
    follower = Follow.objects.filter(community_id = id).count()
    comment_list = Communityforum.objects.filter(community_id = id).order_by('-datetime')
    community_list = Follow.objects.filter(user_id = request.user.id)
    context = {
        'community':community,
        'follower':follower,
        'comment_list':comment_list,
        'community_list':community_list,
    }
    return render(request, 'frontend/community_details.html',context)

@login_required
def add_communitycontent(request, id): 
    if request.method == 'POST': 
        profile_pic = request.FILES.get('profile_image') 
        fs = FileSystemStorage()
        fname = fs.save(profile_pic.name, profile_pic)
        upload_file_url = fs.url(fname) 
        content = request.POST.get('content')
        return redirect('core:publish_communitycontent', cid=id, image=profile_pic,content=content) 

    context = {
        'id':id
    }
    return render(request,'frontend/add_communitycontent.html',context)

@login_required
def publish_communitycontent(request, cid,image, content): 
    user_id = request.user.id 
    if request.method == 'POST':
        Communityforum.objects.create(user_id = user_id, community_id = cid, image = image, content=content)
        return redirect('core:community_details', cid)
    context = {
        'content':content,
        'image':image,
        'cid':cid,
    }
    return render(request, 'frontend/publish_communitycontent.html', context)

@login_required
def add_like(request):
    if request.is_ajax():
        content_id = int(request.GET.get('content_id'))
        communityforum = Communityforum.objects.get(id = content_id)
        notification_recever = communityforum.user.id
        user_id = request.user.id 
        user = User.objects.get(id = user_id)
        Like.objects.create(user_id = user_id, communityforum_id = content_id)
        ntfc_title = "{} liked your community content".format(user.username)
        notification_msg = "{} liked your community content".format(user.username)
        Notification.objects.create(user_id = notification_recever,title= ntfc_title, message=notification_msg)
        return JsonResponse({"message":"Liked"})

@login_required
def add_usercomment(request,forum_id):
    user_id = request.user.id
    user = User.objects.get(id = user_id)
    community_forum = Communityforum.objects.get(id=forum_id)
    comments_list = Usercomment.objects.filter(commented_forum_id=forum_id).order_by('-datetime') 

    page = request.GET.get('page', 1)
    paginator = Paginator(comments_list, 5)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        Usercomment.objects.create(commented_user_id= user_id,commented_forum_id=forum_id,comment_text=comment_text)
        
        community_url = "/add-usercomment/{}".format(forum_id)
        ntfc_title = "{} commented on your community content".format(user.username)
        notification_msg = """
        <p style="font-size:16px; margin-bottom:10px;"><strong>{}</strong> commented on your community content. Check the comment by clicking the following button. </p>
        <a style="float:left;width:150px;padding:10px;display:inline-block; margin-right:10px;background:green;text-decoration:none;border-radius:4px;font-size:16px;text-align:center;color:#fff" href="{}">Check Comment</a>
        """.format(user.username,community_url)
        Notification.objects.create(user_id = community_forum.user.id,title= ntfc_title, message=notification_msg)
        
        return redirect('core:add_usercomment', forum_id)
    
    context = {
        'comments_list':numbers,
        'community_forum':community_forum,
    }
    return render(request, 'frontend/add_usercomment.html',context)

@login_required
def comment_edit(request, id):
    if request.method == 'POST': 
        new_comment = request.POST.get('new_comment')
        user_comment = Usercomment.objects.get(id=id)
        user_comment.comment_text = new_comment
        user_comment.save()
        return redirect('core:add_usercomment',user_comment.commented_forum.id )

@login_required
def comment_delete(request, id): 
    user_comment = Usercomment.objects.get(id=id)
    user_comment.delete() 
    return redirect('core:add_usercomment',user_comment.commented_forum.id )


import json
def get_places(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        places = Community.objects.filter(name__icontains=q)
        results = []
        for pl in places:
            place_json = {}
            place_json = pl.name
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def team_default(request):
    user_id = request.user.id 
    try:
        friend_list = Friend.objects.get(user_id = user_id)  
    except:
        friend_list = None 
        
    team_list = Team.objects.all()   
    context = {
        'friend_list':friend_list,
        'team_list':team_list,
    }
    return render(request, 'frontend/team_default.html', context)

def create_team(request):
    admin_id = request.user.id
    hash_tags = Hashtag.objects.filter(status = True)
    try:
        friend_list = Friend.objects.get(user_id = request.user.id) 
    except :
        friend_list = None
    
    if request.method == "POST": 
        bg_image = request.FILES.get('background_image') 
        fs = FileSystemStorage()
        fname = fs.save(bg_image.name, bg_image)
        upload_file_url = fs.url(fname) 

        logo_image = request.FILES.get('team_logo') 
        fs = FileSystemStorage()
        fname = fs.save(logo_image.name, logo_image)
        upload_file_url = fs.url(fname) 
        team_name = request.POST.get("team_name")
        tag_list = request.POST.getlist('tags[]')
        team_member_list = request.POST.getlist('members[]')
        hashtag_size = len(tag_list)
        team_member_size = len(team_member_list)
        if hashtag_size > 8 :
            messages.error(request, "You have selected More than 8 Hash Tags")
            return redirect('core:create_team')
        else:
            if team_member_size > 10:
                messages.error(request, "You have selected More than 8 Hash Tags")
                return redirect('core:create_team')
            else:
                team = Team.objects.create(name=team_name, admin_id = admin_id, logo=logo_image, background_image= bg_image)  
                for tag in tag_list:
                    tag = Hashtag.objects.get(id = tag)
                    team.hastag.add(tag)   

                if team_member_list:
                    for member in team_member_list:  
                        team_invite = Teaminvite.objects.create(team_id =team.id, member_id = member)
                        ntfc_title = "Invaitation to Join {} Team".format(team_name) 
                        accept_url = "/invaitation-accept/{}/{}".format(team.id, team_invite.id)
                        decline_url = "/invaitation-decline/{}/{}".format(team.id, team_invite.id)
                        notification_msg = """
                            <p style="font-size:16px; margin-bottom:10px;"><strong>{}</strong> sent you invaitation to join the the team <strong>{}</strong>.</p> <br> 
                            <a style="float:left;width:100px;padding:10px;display:inline-block; margin-right:10px;background:green;text-decoration:none;border-radius:4px;font-size:16px;text-align:center;color:#fff" href="{}">Accept</a>
                            <a style="float:left;width:100px;padding:10px;display:inline-block; margin-right:10px;background:red;text-decoration:none;border-radius:4px;font-size:16px;text-align:center;color:#fff" href="{}">Decline</a> 
                        """.format(request.user.username,team_name,accept_url,decline_url )
                        Notification.objects.create(user_id = member,title= ntfc_title, message=notification_msg)
                        


                admin_member = User.objects.get(id=request.user.id)
                team.team_member.add(admin_member)
                return redirect('core:team_details', team.id)

    context = {
        'hash_tags':hash_tags,
        'friend_list':friend_list,
    }
    return render(request, 'frontend/create_team.html', context)

def team_details(request, id):
    team = Team.objects.get(id=id)
    context = {
        'team':team
    }
    return render(request, 'frontend/team_details.html', context)

def team_update(request, id):
    team = Team.objects.get(id = id)
    if request.method == "POST":
        bg_image = request.FILES.get('bg_image')  
        logo_image = request.FILES.get('logo_image') 
        
        if bg_image: 
            fs = FileSystemStorage()
            fname = fs.save(bg_image.name, bg_image)
            upload_file_url = fs.url(fname) 
            team.background_image = bg_image

        if logo_image: 
            fs = FileSystemStorage()
            fname = fs.save(logo_image.name, logo_image)
            upload_file_url = fs.url(fname) 
            team.logo = logo_image
            
        team.save()
        return redirect('core:team_details', id)

def invaitation_decline(request, team_id,invite_id):
    user = User.objects.get(id = request.user.id)
    team_invite = Teaminvite.objects.get(id = invite_id)
    if team_invite.receive_status:
        messages.success(request, "You have already Accepted this invaitation")
        return redirect("core:notification_list")

    if not team_invite.status:
        messages.success(request, "You have already declined this invaitation")
        return redirect("core:notification_list")

    team = Team.objects.get(id = team_id)
    team_invite.status = False 
    team_invite.save()
    ntfc_title = "{} declined the Invaitation".format(user.username, team.name)  
    notification_msg = """
        <p style="font-size:16px; margin-bottom:10px;">"<strong>{}</strong> declined the invaitation to join the Team <strong>{}</strong> "</p> <br> 
    """.format(user.username, team.name ) 
    Notification.objects.create(user_id = team.admin.id, title= ntfc_title, message=notification_msg) 
    return redirect("core:notification_list")

def invaitation_accept(request, team_id,invite_id): 

    team = Team.objects.get(id = team_id)
    user = User.objects.get(id = request.user.id)
    user_check = user.team_set.filter(id = team_id)
    team_invite = Teaminvite.objects.get(id = invite_id) 
 
    if not team_invite.status:
        messages.success(request, "You have already declined this invaitation")
        return redirect("core:notification_list")
    if user_check.exists():
        messages.success(request, "You have already Accepted this invaitation")
        return redirect("core:notification_list")
    else: 
        team_invite.receive_status = True
        team_invite.save()
        team.team_member.add(user)
        ntfc_title = "{} jointed the Team {}".format(user.username, team.name) 
        team_url = "/team-details/{}".format(team.id)
        notification_msg = """
            <p style="font-size:16px; margin-bottom:10px;">"<strong>{}</strong> accepted the invaitation and jointed the Team <strong>{}</strong> "</p> <br> 
            <a style="float:left;width:130px;padding:10px;display:inline-block; margin-right:10px;background:green;text-decoration:none;border-radius:4px;font-size:16px;text-align:center;color:#fff" href="{}">Check Team</a> 
        """.format(user.username, team.name,team_url ) 
        Notification.objects.create(user_id = team.admin.id, title= ntfc_title, message=notification_msg)


        return redirect('core:team_details',team_id)

def notification_list(request):
    user_id = request.user.id
    notifications = Notification.objects.filter(user_id = user_id).order_by('-date')

    page = request.GET.get('page', 1)
    paginator = Paginator(notifications, 5)
    try:
        ntfc_list = paginator.page(page)
    except PageNotAnInteger:
        ntfc_list = paginator.page(1)
    except EmptyPage:
        ntfc_list = paginator.page(paginator.num_pages)


    context = {
        'notifications':ntfc_list
    }
    return render(request,'frontend/notification_list.html', context)

def notification_details(request, id):
    notification = Notification.objects.get(id=id)
    notification.view_status = True
    notification.save()
    context = {
        'notification':notification
    }
    return render(request, 'frontend/notification_details.html', context)


def add_team_member(request, team_id):
    return render(request, 'frontend/add_team_member.html')


def search_team_player(request):
    user = User.objects.get(id = request.user.id)
    team_list = user.team_set.all()  
    if request.method == 'POST':
        query = request.POST.get('query')
        query_team = Team.objects.filter(name__icontains = query)
        query_player = User.objects.filter(username__icontains = query)
        context = {
            'team_list':team_list,
            'query_team':query_team,
            'query_player':query_player,
        }
    else:
        context = {
            'team_list':team_list
        }
    return render(request, 'frontend/search_team_player.html', context)

def player_profile(request, id):
    player = User.objects.get(id = id)
    team_list = player.team_set.all()
    friend_list = player.friend_set.all()
    context = {
        'player':player,
        'team_list':team_list,
        'friend_list':friend_list,
    }
    return render(request, 'frontend/player_profile.html',context)

def player_profile_update(request): 
    id = request.user.id
    player = Mainuser.objects.get(user_id = id) 
    print(player)
    if request.method == "POST":
        bg_image = request.FILES.get('bg_image')  
        logo_image = request.FILES.get('logo_image') 
        print(bg_image)
        print(logo_image)
        if bg_image: 
            fsb = FileSystemStorage()
            fnameb = fsb.save(bg_image.name, bg_image)
            upload_file_url = fsb.url(fnameb) 
            player.bgimage = bg_image
            player.save()

        if logo_image: 
            fs = FileSystemStorage()
            fname = fs.save(logo_image.name, logo_image)
            upload_file_url = fs.url(fname) 
            player.profile_pic = logo_image
            
        player.save()
        return redirect('core:player_profile', id) 

def create_inappropiate_post(request, forum_id, community_id):
    user_id = request.user.id
    Foruminappropiate.objects.create(user_id = user_id, forum_id = forum_id)
    return redirect('core:community_details', community_id)

def send_friend_request(request, recever_id):
    sender_id = request.user.id
    sender = User.objects.get(id = sender_id)  
    friend_request = Friendrequest.objects.create(serner_id = sender_id, recever_id = recever_id) 
    ntfc_title = "{} send you friend request".format(sender.username) 
    accept_url = "/friend-request-accept/{}/{}".format(sender_id,friend_request.id )
    decline_url = "/friend-request-decline/{}/{}".format(sender_id, friend_request.id)
    notification_msg = """
        <p style="font-size:16px; margin-bottom:10px;"><strong>{}</strong> sent you friend request</p> <br> 
        <a style="float:left;width:100px;padding:10px;display:inline-block; margin-right:10px;background:green;text-decoration:none;border-radius:4px;font-size:16px;text-align:center;color:#fff" href="{}">Accept</a>
        <a style="float:left;width:100px;padding:10px;display:inline-block; margin-right:10px;background:red;text-decoration:none;border-radius:4px;font-size:16px;text-align:center;color:#fff" href="{}">Decline</a> 
    """.format(sender.username,accept_url,decline_url )
    Notification.objects.create(user_id = recever_id,title= ntfc_title, message=notification_msg) 
    return redirect('core:player_profile',recever_id)

def friend_request_accept(request, sender_id, request_id): 
    friend_request = Friendrequest.objects.get(id = request_id)
    if friend_request.status == False:
        messages.success(request,"You have already cancelled the friend request")
        return redirect('core:notification_list') 

    if friend_request.accepted_status == True:
        messages.success(request,"You have already accepted the friend request")
        return redirect('core:notification_list')

    sender = User.objects.get(id = sender_id) 
    user_id = request.user.id
    friend_object, created = Friend.objects.get_or_create(user_id = user_id) 
    friend_object.friend_list.add(sender)

    user = User.objects.get(id = user_id)
    friend_object_sender, created = Friend.objects.get_or_create(user_id = sender_id)
    friend_object_sender.friend_list.add(user)

    
    friend_request.accepted_status = True
    friend_request.save()

    ntfc_title = "{} accepted friend request".format(user.username) 
    profile_url = '/player-profile/{}'.format(user_id)
    notification_msg = """
        <p style="font-size:16px; margin-bottom:10px;"><strong>{}</strong> friend your friend request. </p> <br> 
        <a style="float:left;width:130px;padding:10px;display:inline-block; margin-right:10px;background:green;text-decoration:none;border-radius:4px;font-size:16px;text-align:center;color:#fff" href="{}">View Profile</a> 
    """.format(user.username,profile_url )
    Notification.objects.create(user_id = sender_id,title= ntfc_title, message=notification_msg) 
    return redirect('core:player_profile',user_id)


def friend_request_decline(request,sender_id, request_id): 
    friend_request = Friendrequest.objects.get(id = request_id)
    if friend_request.status == False:
        messages.success(request,"You have already cancelled the friend request")
        return redirect('core:notification_list') 

    if friend_request.accepted_status == True:
        messages.success(request,"You have already accepted the friend request")
        return redirect('core:notification_list') 

    friend_request.accepted_status = False
    friend_request.status = False
    friend_request.save()

    user = User.objects.get(id = request.user.id)
    sender = User.objects.get(id = sender_id)

    ntfc_title = "{} declined your friend request".format(user.username)  
    notification_msg = """
        <p style="font-size:16px; margin-bottom:10px;"><strong>{}</strong> declined your friend request. </p> 
    """.format(user.username )
    Notification.objects.create(user_id = sender_id,title= ntfc_title, message=notification_msg) 

    return redirect('core:notification_list')

def friend_request_cancel(request, recever_id):
    sender_id = request.user.id
    request = Friendrequest.objects.filter(serner_id = sender_id, recever_id = recever_id)
    request.delete()
    return redirect('core:player_profile',recever_id)

def joining_team_request(request, team_id,team_admin_id): 
    user_id = request.user.id
    team = Team.objects.get(id = team_id)
    user = User.objects.get(id = user_id)
    total_team_joined = user.team_set.all().count()
    if total_team_joined >= 5:
        messages.warning(request, "You have already joined 5 teams")
        return redirect('core:team_details', team_id)
    else:
        total_invite = Teaminvite.objects.filter(member_id = user_id, receive_status=False,status=True).count()
        total_active = total_team_joined + total_invite
        if total_active >= 5:
            messages.warning(request, "You have joined {} team and you have send {} invaitations").format(total_team_joined,total_invite)
        else:
            team_invite = Teaminvite.objects.create(team_id = team_id, member_id = user_id)
            ntfc_title = "Invaitation to Join {} Team".format(team.name) 
            accept_url = "/invaitation-accept/{}/{}".format(team.id, team_invite.id)
            decline_url = "/invaitation-decline/{}/{}".format(team.id, team_invite.id)
            notification_msg = """
                <p style="font-size:16px; margin-bottom:10px;"><strong>{}</strong> sent you invaitation to join the the team <strong>{}</strong>.</p> <br> 
                <a style="float:left;width:100px;padding:10px;display:inline-block; margin-right:10px;background:green;text-decoration:none;border-radius:4px;font-size:16px;text-align:center;color:#fff" href="{}">Accept</a>
                <a style="float:left;width:100px;padding:10px;display:inline-block; margin-right:10px;background:red;text-decoration:none;border-radius:4px;font-size:16px;text-align:center;color:#fff" href="{}">Decline</a> 
            """.format(request.user.username,team.name,accept_url,decline_url )
            Notification.objects.create(user_id = team_admin_id,title= ntfc_title, message=notification_msg) 

    return redirect('core:team_details', team_id)

    

    