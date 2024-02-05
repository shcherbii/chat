from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return HttpResponse("You already have account and login")
    else:
        if request.method == 'POST':
            user_form = RegistrationForm(request.POST)
            # print(user_form)

            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                user_form.check_password()
                data = user_form.cleaned_data
                new_user.set_password(data['password'])
                new_user.save()

                user = authenticate(request, username=data['username'], password=data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('index') # HttpResponse("user auth and login")
                else:
                    return redirect('login')
            
                # return render(request, 'user/login.html')
        else:
            user_form = RegistrationForm()

        return render(request, 'user/register.html', {'user_form': user_form})