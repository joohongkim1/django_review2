from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout


def signup(request):
    if request.method == 'POST':
        # 회원가입 로직
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:  # == 'GET'
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.method == 'POST':
        # 로그인 로직
        form = AuthenticationForm(request, request.POST)
        if form.is_valid(): # 사용자가 넘겨준 아이디와 비밀번호가 일치한다면
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
        context ={'form': form}
        return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')
