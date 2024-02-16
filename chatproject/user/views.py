from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserEditform, ProfileEditform
from .models import Profile
from django.http import HttpResponse
from chat.views import append_user
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return HttpResponse("You already have account and login")
    else:
        if request.method == 'POST':
            user_form = RegistrationForm(request.POST)

            if user_form.is_valid():
                user_form.check_password()

                new_user = user_form.save(commit=False)
                data = user_form.cleaned_data

                new_user.set_password(data['password'])
                new_user.save()

                Profile.objects.create(user=new_user)
                user = authenticate(request, username=data['username'], password=data['password'])
                append_user(user)

                login(request, user)
                return redirect('index')
        else:
            user_form = RegistrationForm()

        return render(request, 'user/register.html', {'user_form': user_form})
    

@login_required
def profile(request, username):
    profile = get_object_or_404(Profile, user__username = username)
    return render(request, 'user/profile.html', {'profile': profile})


@login_required
def edit(request):

    if request.method == 'POST':
        user_form = UserEditform(instance=request.user, data=request.POST)
        profile_form = ProfileEditform(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditform(instance=request.user)
        profile_form = ProfileEditform(instance=request.user.profile)
        
    profile = get_object_or_404(Profile, user = request.user)

    return render(request, 'user/edit.html', {'user_form': user_form, 'profile_form': profile_form, 'profile': profile})