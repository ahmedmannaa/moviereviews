from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import UserCreateForm,AuthForm
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

def signupaccount(req):
    if req.method == 'GET':
        return render(req, 'signupaccount.html', {
            'form':UserCreateForm
        })
    else:
        if req.POST['password1'] == req.POST['password2']:
            try:
                user = User.objects.create_user(req.POST['username'], password=req.POST['password1'])
                user.save()
                login(req, user)
                return redirect('home')
            except IntegrityError:
                return render(req, 'signupaccount.html', {
                    'form': UserCreateForm,
                    'error': 'Username already taken. Choose new username.'
                })
        else:
            return render(req,'signupaccount.html',{
                'form':UserCreateForm,
                'error':'Passwords do not match'
            })

@login_required
def logoutaccount(req):
    logout(req)
    return redirect('home')

def loginaccount(req):
    if req.method == 'GET':
        return render(req,'loginaccount.html',{
            'form': AuthForm
        })
    else:
        user = authenticate(req, username=req.POST['username'],
                            password=req.POST['password'])
        if user is None:
            return render(req,'loginaccount.html',
                          {
                              'form': AuthForm,
                              'error': 'username and password do not match'
                          })
        else:
            login(req,user)
            return redirect('home')

