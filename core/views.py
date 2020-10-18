from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import Community, Follow, Communityforum, Like, Usercomment
from django.contrib.auth.decorators import login_required
from django.core.files.storage import  FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

def add_like(request):
    if request.is_ajax():
        content_id = int(request.GET.get('content_id'))
        user_id = request.user.id
        Like.objects.create(user_id = user_id, communityforum_id = content_id)
        return JsonResponse({"message":"Liked"})


def add_usercomment(request,forum_id):
    user_id = request.user.id
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
        return redirect('core:add_usercomment', forum_id)
    
    context = {
        'comments_list':numbers,
        'community_forum':community_forum,
    }
    return render(request, 'frontend/add_usercomment.html',context)
 
def comment_edit(request, id):
    if request.method == 'POST': 
        new_comment = request.POST.get('new_comment')
        user_comment = Usercomment.objects.get(id=id)
        user_comment.comment_text = new_comment
        user_comment.save()
        return redirect('core:add_usercomment',user_comment.commented_forum.id )

def comment_delete(request, id): 
    user_comment = Usercomment.objects.get(id=id)
    user_comment.delete() 
    return redirect('core:add_usercomment',user_comment.commented_forum.id )



















from .models import Agency, Property

def property(request, name):
    agency = Agency.objects.get(name=name)
    if agency.domain_status:
        property_list = Property.objects.filter(agency_id = agency.id)
        context = {
            'property_list':property_list,
            'agency':agency
        }
        return render(request, 'accounts/agency_property.html', context)

    else:
        return HttpResponse("Sorry!! This agency is not able to show their propery")




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