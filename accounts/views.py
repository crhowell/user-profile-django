from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import ProfileForm, ChangePasswordForm
from .models import Profile


@login_required(login_url='/accounts/sign_in/')
def profile_show(request, user_pk):
    profile = get_object_or_404(Profile, user=user_pk)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required(login_url='/accounts/sign_in/')
def profile_edit(request):
    usr_profile = Profile.objects.get(user=request.user)
    form = ProfileForm(initial={
        'first_name': usr_profile.first_name,
        'last_name': usr_profile.last_name,
        'email': usr_profile.email,
        'short_bio': usr_profile.short_bio,
        'date_of_birth': usr_profile.date_of_birth})
    if request.method == 'POST':
        if form.is_valid():
            form = ProfileForm(request.POST)
            form.save()
            messages.success(request, 'Profile saved!')
            return HttpResponseRedirect(reverse('accounts:profile', args=(request.user.pk,)))
        messages.error(request, 'There was an error with your changes.')
        return render(request, 'accounts/profile_edit.html', {'form': form})
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required(login_url='/accounts/sign_in')
def change_password(request):
    form = ChangePasswordForm()
    if request.method == 'POST':
        pass
    return render(request, 'accounts/change_password.html', {'form': form})


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile', args=(request.user.pk,))
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            Profile.create_profile(user)
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:profile', args=(request.user.pk,)))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))
