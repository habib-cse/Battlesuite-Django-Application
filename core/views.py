from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from .models import (TestConnection, Community, Follow, Communityforum, 
                    LoadingScreenAdmin, Like, LoadingScreen, Usercomment, 
                    Game, GameTeam, Team, TeamUser, TournamentTeamUser, 
                    TournamentTeam, Tournament, Challenge, TournamentInvite, 
                    TournamentTeam, TournamentRound)
from .forms import TournamentForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import  FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register
from django.contrib.auth.models import User 
from django.utils.formats import localize
import dateutil.parser
import random
from django.utils import timezone

team_size_choices = ["1 VS 1","2 VS 2","3 VS 3","4 VS 4","5 VS 5"]
team_number_choices = ["2 Teams", "4 Teams", "8 Teams"]
game_length_choices = ["40 Minutes","60 Minutes","80 Minutes"]

@register.filter
def split(string, key):
    return string.split(key)[0]

# Create your views here.
def home(request):
    return render(request,'frontend/index.html')

def delete_test(request):
    all_connections = TestConnection.objects.all()
    for connection in all_connections:
        connection.delete()
    return redirect(reverse('core:test'))

def get_more_tables(request):
    all_connections = TestConnection.objects.all()

    context = {
        "current_pk": 44,
        "all_connections": all_connections,
        "ready_list": [244, 245],
    }
    return render(request, 'frontend/testpagetable.html', context)
    # return HttpResponse("<p>tablesssss</p>")

def testpage(request):
    # if request.method == "POST":
    #     delete_test()
    new_connection = TestConnection()
    new_connection.save()

    current_pk = new_connection.pk
    all_connections = TestConnection.objects.all()

    context = {
        "usernames": ["Adam", "Bart", "Casey"],
        "current_pk": current_pk,
        "all_connections": all_connections,
        "ready_list": [244, 245],
    }
    return render(request, 'frontend/testpage.html', context)


@login_required()
def create_tournament(request):
    user_team = TeamUser.objects.get(user=request.user).team
    if request.method=="GET":
        tournament = None
        user_team = TeamUser.objects.get(user=request.user).team
        if "use_tournament" in request.session:
            if request.session["use_tournament"]:
                tournament_pk = request.session["use_tournament"]
                tournament = Tournament.objects.get(pk = tournament_pk)
        context = {
            "team_size_choices" : team_size_choices,
            "team_number_choices" : team_number_choices,
            "game_length_choices" : game_length_choices,
            "tournament": tournament
        }
        return render(request, "frontend/create-my-tournament.html", context=context)

    elif request.method=="POST":
        form = TournamentForm(request.POST)
        if "use_tournament" in request.session:
            if request.session["use_tournament"]:
                tournament_pk = request.session["use_tournament"]
                tournament = Tournament.objects.get(pk = tournament_pk)

                
            else:
                tournament = Tournament(creator=request.user)
        else:
            tournament = Tournament(creator=request.user)
        
        setattr(tournament, 'name', form.data["name"])
        setattr(tournament, 'game_name' ,form.data["game_name"])
        setattr(tournament, 'date' ,dateutil.parser.parse(form.data["date"]))
        setattr(tournament, 'game_length' ,int(split(form.data["game_length"], " ")))
        setattr(tournament, 'description' ,form.data["description"])
        setattr(tournament, 'platform' ,form.data["platform"])
        setattr(tournament, 'player_amount' ,form.data["player_amount"])
        setattr(tournament, 'number_of_teams' ,form.data["number_of_teams"])

        tournament.save()
        request.session["use_tournament"] = {"tournament": tournament.pk}

        try:
            relation = TournamentTeam.objects.get(tournament=tournament, team=user_team)
        except:
            relation = TournamentTeam(tournament=tournament, team=user_team)
            relation.save()

        return edit_tournament(request)

@login_required()
def edit_tournament(request):
    user_team = TeamUser.objects.get(user=request.user).team

    tournament = Tournament.objects.get(pk=request.session.get('use_tournament', None)["tournament"])
    
    if request.method=="POST":
        if "Challenge-Team" in request.POST:
            new_challenge = Challenge(tournament=tournament, 
                                        host_team=user_team,
                                        challenged_team=Team.objects.get(name=request.POST["Challenge-Team"]))
            new_challenge.save()
        elif "Invite-TeamMember" in request.POST:
            print(request.POST["Invite-TeamMember"])
            new_invite = TournamentInvite(tournament=tournament,
                                            user=User.objects.get(pk=request.POST["Invite-TeamMember"]))
            new_invite.save()

    challenged_teams = Challenge.objects.filter(host_team=user_team, tournament=tournament)
    challenged_teams = [relation.challenged_team for relation in challenged_teams]

    all_teams = [team for team in Team.objects.all()]
    all_teams.remove(user_team)

    teammembers = TeamUser.objects.filter(team=user_team)
    teammembers = [relation.user for relation in teammembers if relation.user != request.user]

    invited_teammembers = [TournamentInvite.objects.filter(tournament=tournament, user=tm) for tm in teammembers]
    invited_teammembers = [queryset[0] for queryset in invited_teammembers if len(queryset)>0]
    
    invited_teammembers = [relation.user.username for relation in invited_teammembers]
    context = {
        "all_teams": all_teams,
        "challenged_teams": challenged_teams,
        "teammembers": teammembers,
        "invited_teammembers": invited_teammembers,
        "user_team": user_team
    }

    return render(request, "frontend/create-my-tournament-teams.html", context)

def tournament_mytournament(request):
    if request.method == "GET":
        tournaments = Tournament.objects.filter(creator=request.user)
        tournaments = [[tournament, int((timezone.now() - tournament.date).total_seconds() / (60 * 60))] for tournament in tournaments]
        print(tournaments)
        context = {
            "path": "mytournament",
            "tournaments": tournaments,
        }
        return render(request, "frontend/tournament-page-mytournament.html", context)

    elif request.method == "POST":
        if 'Edit Tournament' in request.POST:
            tournament = request.POST['Tournament-To-Edit']
            request.session["use_tournament"] = tournament
            request.method = "GET"
            return create_tournament(request)
        elif 'Cancel Tournament' in request.POST:
            print(request.POST['Tournament-To-Edit'])
            tournament_pk = request.POST['Tournament-To-Edit']
            tournament = Tournament.objects.get(pk=tournament_pk)
            tournament.delete()
            request.method = "GET"
            return tournament_mytournament(request)
        elif 'New Tournament.x' in request.POST:
            request.method = "GET"
            request.session["use_tournament"] = None
            return create_tournament(request)

def tournament_challenges(request):
    user_team = TeamUser.objects.get(user=request.user).team
    challenges = Challenge.objects.filter(challenged_team=user_team)
    
    context = {
        "path": "challenges",
        "challenges": challenges,
    }

    if request.method == "GET":
        return render(request, "frontend/tournament-page-challenges.html", context)

    elif request.method == "POST":
        if "Decline Challenge" in request.POST:
            tournament = request.POST['Tournament-To-Edit']
            tournament = Tournament.objects.get(pk=tournament)
            challenge_to_delete = Challenge.objects.get(tournament=tournament, challenged_team=user_team)
            challenge_to_delete.delete()
            request.method = "GET"
            return tournament_challenges(request)
        elif "Accept Challenge" in request.POST:
            tournament = request.POST['Tournament-To-Edit']
            tournament = Tournament.objects.get(pk=tournament)
            tournament_team = TournamentTeam(tournament=tournament, team=user_team)
            tournament_team.save()
            challenge_to_delete = Challenge.objects.get(tournament=tournament, challenged_team=user_team)
            challenge_to_delete.delete()
            request.method = "GET"
            return tournament_challenges(request)

def tournament_invites(request):
    user_team = TeamUser.objects.get(user=request.user).team
    invites = TournamentInvite.objects.filter(user=request.user)

    context = {
        "path": "invites",
        "invites": invites,
        "user_team": user_team,
    }
    if request.method == "GET":
        return render(request, "frontend/tournament-page-invites.html", context)

    elif request.method == "POST":
        if "Decline Invite" in request.POST:
            tournament = request.POST['Tournament-To-Edit']
            tournament = Tournament.objects.get(pk=tournament)
            invite_to_delete = TournamentInvite.objects.get(tournament=tournament, user=request.user)
            invite_to_delete.delete()
            request.method = "GET"
            return tournament_challenges(request)
        elif "Accept Invite" in request.POST:
            tournament = request.POST['Tournament-To-Edit']
            tournament = Tournament.objects.get(pk=tournament)
            # tournament_team = TournamentTeam(tournament=tournament, team=user_team)
            # tournament_team.save()
            invite_to_delete = TournamentInvite.objects.get(tournament=tournament, user=request.user)
            invite_to_delete.delete()
            return tournament_challenges(request)

def prepare_tournament_games(tournament):
    avaliable_teams = [i.team for i in TournamentTeam.objects.filter(tournament=tournament)]
    tournamentround = TournamentRound(tournament=tournament)
    tournamentround.save()
    while len(avaliable_teams)%2 == 0 and len(avaliable_teams)>0:
        game = Game(tournament=tournament, duration=tournament.game_length)

        teamA = random.choice(avaliable_teams)
        avaliable_teams.remove(teamA)

        teamB = random.choice(avaliable_teams)
        avaliable_teams.remove(teamB)

        players_teamA = [i.user for i in TournamentTeamUser.objects.filter(tournament=tournament, team=teamA)]
        players_teamB = [i.user for i in TournamentTeamUser.objects.filter(tournament=tournament, team=teamB)]

        game.save()

        for player in players_teamA:
            game.players.add(player)
        
        for player in players_teamB:
            game.players.add(player)

        game_teamA = GameTeam(game=game, team=teamA)
        game_teamB = GameTeam(game=game, team=teamB)

        game_teamA.save()
        game_teamB.save()

        tournamentround.games.add(game)

def check_player_conectivity(Game, LoadingScreen):
    print(Game.players.all())
    print(LoadingScreen.players.all())
    for player in Game.players.all():
        if player not in LoadingScreen.players.all():
            return False
    return True

@login_required()
def tournament_start_waiting(request):
    user_team = TeamUser.objects.get(user=request.user).team
    tournament = Tournament.objects.get(creator=1)
    try:
        tournamentround = TournamentRound.objects.get(tournament=tournament)
    except:
        prepare_tournament_games(tournament)

    games_in_tournament = Game.objects.filter(tournament=tournament)
    for game in games_in_tournament:
        if request.user in game.players.all():
            break

    if len(LoadingScreen.objects.filter(Game=game)) != 0:
        loadingscreen = LoadingScreen.objects.filter(Game=game)[0]
    else:
        loadingscreen = LoadingScreen(Game=game)
        loadingscreen.save()
    
    if request.user not in loadingscreen.players.all():
        loadingscreen.players.add(request.user)

    teamA = user_team
    teamB = GameTeam.objects.filter(game=game).exclude(team=teamA)[0].team
    context = {
        "game": game,
        "teamA": teamA,
        "teamB": teamB
    }

    if check_player_conectivity(game, loadingscreen):
        adminA = teamA.admin
        adminB = teamB.admin

        chosen_admin = random.choice([adminA, adminB])
        try: 
            loadingscreenadmin = LoadingScreenAdmin.objects.get(loadingscreen=loadingscreen)
        except:
            loadingscreenadmin = LoadingScreenAdmin(loadingscreen=loadingscreen, admin=chosen_admin)
            loadingscreenadmin.save()
        return tournament_admin_start(request)

    return render(request, "frontend/start-tournament-loading-page.html", context)

def tournament_admin_start(request):
    user_team = TeamUser.objects.get(user=request.user).team
    tournament = Tournament.objects.get(creator=1)

    games_in_tournament = Game.objects.filter(tournament=tournament)
    for game in games_in_tournament:
        if request.user in game.players.all():
            break
    
    enemy_team = [i.team for i in GameTeam.objects.filter(game=game) if i.team != user_team][0]
    
    teammembers = [i.user for i in TournamentTeamUser.objects.filter(tournament=tournament, team=user_team)]
    opponenets = [i.user for i in TournamentTeamUser.objects.filter(tournament=tournament, team=enemy_team)]

    loadingscreen = LoadingScreen.objects.get(Game=game)
    loadingscreenadmin = LoadingScreenAdmin.objects.get(loadingscreen=loadingscreen)

    if request.method == "POST":
        print(request.POST)
        if "Admin Ready" in request.POST:
            loadingscreenadmin.ready = True
            loadingscreenadmin.save()
        
    context = {
        "game": game,
        "teamA": user_team,
        "teamB": enemy_team,
        "teammembers": teammembers,
        "opponenets": opponenets,
        "loadingscreenadmin": loadingscreenadmin
    }

    if request.user == loadingscreenadmin.admin:
        return render(request, "frontend/start-tournament-set-up-admin.html", context=context)
    else:
        return render(request, "frontend/start-tournament-set-up-waiting.html",  context=context)

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
        user_id = request.user.id
        Like.objects.create(user_id = user_id, communityforum_id = content_id)
        return JsonResponse({"message":"Liked"})

@login_required
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



