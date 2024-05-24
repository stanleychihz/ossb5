from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User, auth
from . models import *
from home.models import *
from django.contrib import messages


# Create your views here.

def home(request):

    x = Static.objects.all()
    options = Icon2.objects.all()
    #inbox = Messages.objects.all().aggregate(inbox=Sum('msg')) 
    inbox = Messages.objects.filter(pkv='1987').count()

    return render(request, 'home.html', {'x': x,
                                         'options': options,
                                         'inbox': inbox})

def xbase(request):
    x = Static.objects.all()
    return render(request, 'xbase.html', {'x': x})


def signup(request):

    x = Static.objects.all()
    msg = 'Login Now'
    

    if request.method == 'POST':

        reg = request.POST['reg']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        nickname = request.POST['nickname']
        Stu = Students.objects.filter(reg=reg)
        
        if len(reg) == 0 or len(nickname) == 0 or len(password1) == 0 or len(password2) == 0:
            messages.info(request, 'Fields cannot be empty')
            return render(request, 'signup.html')
        else:
            if password1 == password2:
                if User.objects.filter(username=reg).exists():
                    messages.info(request, 'Student already exists')
                    return render(request, 'signup.html')
                elif len(password1) < 8:
                    messages.info(request, 'Password should be at least 8 characters')
                    return render(request, 'signup.html')
                else:
                    reg_no = ' '         
                    for stu in Stu:
                        name = stu.name
                        reg_no = stu.reg
                    if Students.objects.filter(reg=reg_no).exists():
                        new_user = User.objects.create_user(username=reg,
                                                        password=password1,
                                                        first_name=nickname)
                        new_user.save()
                        messages.info(request, 'Registration successful' + ' ' + name)
                        return render(request, 'signup.html', {'msg': msg})
                    else:
                        messages.info(request, 'Student does not exist at University of Zimbabwe')
                        return render(request, 'signup.html')
            else:
                messages.info(request, 'Passwords not matching')
                return render(request, 'signup.html')
    else:
        return render(request, 'signup.html', {'x': x})

def lgn(request):

    x = Static.objects.all()

    if request.method == 'POST':

        reg = request.POST['reg']
        password = request.POST['password']

        user = authenticate(request, 
                        username=reg,
                        password=password)
        if user is not None:
            login(request, user)
            return render(request, 'i.html')
        else:
            messages.info(request, 'Wrong credidentials')
            return render(request, 'lgn.html')
    else:
        return render(request, 'lgn.html', {'x': x})



def msg(request):
    icons = Icon.objects.all()
    return render(request, 'messages.html', {'icons': icons})

def msg2(request):
    icons = Icon.objects.all()
    return render(request, 'messages2.html', {'icons': icons})

def i(request):

    return render(request, 'i.html')