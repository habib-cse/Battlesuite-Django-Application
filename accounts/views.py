from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from .models import Mainuser
from django.contrib.auth.decorators import login_required
# Create your views here.
def user_register(request):
    try:
        if request.user.is_authenticated:
            return redirect('accounts:user_profile')
        else:
            return render(request, 'accounts/user_register.html')
    except print(0):
        return redirect('accounts:user_profile')
    return render(request, 'accounts/user_register.html')



def profile_create(request): 
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.username) 
        if user.is_staff:
            return redirect('account:user_profile')
        else: 
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                password1 = request.POST['password1']  
                profile_pic = request.FILES.get('profile_image') 
                if password == password1: 
                    user.set_password(password) 
                    user.is_staff = True
                    user.save()
                    group = Group.objects.get(name='muser')
                    user.groups.add(group)   
                    fs = FileSystemStorage()
                    fname = fs.save(profile_pic.name, profile_pic)
                    upload_file_url = fs.url(fname) 
                    Mainuser.objects.create(user_id = user.id,status=True, profile_pic = profile_pic)
            
                    
                    logout(request)
                    messages.success(request, "Profile created successfully") 
                    return redirect('accounts:user_login')
                    
                else:
                    messages.error(request,"Password doesn't match!!")
                    return redirect('accounts:profile_create')
    else:
        return redirect('core:home')

    
    return render(request, 'accounts/profile_create.html')

@login_required
def user_profile(request):
    return render(request, 'accounts/user_profile.html')
    
def user_login(request): 

    valuenext= request.GET.get('next')
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password) 
        if user is not None and valuenext is None:
            login(request, user)
            return redirect('accounts:user_profile') 
        elif user is not None and valuenext is not None:
            login(request, user)
            context= {  
                'valuenext': valuenext 
                } 
            return redirect(valuenext)
        else:
            messages.error(request, 'Username or Password is not correct!') 
    return render(request, 'accounts/user_login.html')

# def profile_update(request):
#     return 

    

@login_required
def become_pro(request):
    return render(request, 'accounts/become_pro.html')

def pro_status(request,str):
    signup_type = str
    user = Mainuser.objects.get(user_id = request.user.id)
    user.pro_status = True
    if signup_type == 'xbox':
        user.pro_signup_type = 'xbox'
    else:
        user.pro_signup_type = 'playstation' 
    user.save()
    return redirect('core:follow_community')
