from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm, CustomUserCreationForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        # 회원가입 로직
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else: # == 'GET'
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/form.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        # 로그인 로직
        form = AuthenticationForm(request, request.POST)
        if form.is_valid(): # 사용자가 넘겨준 아이디와 비밀번호가 일치한다면
            auth_login(request, form.get_user())
            next_page = request.GET.get('next')
            return redirect(next_page or 'articles:index')
    else: # == 'GET'
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('articles:index')


@login_required
def update(request):
    if request.method == 'POST':
        # 수정해주세요 요청이 들어올 때
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        # 수정할 수 있는 페이지를 주세요 요청이 들어올 때
        form = CustomUserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'accounts/form.html', context)


@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:update')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/form.html', context)
