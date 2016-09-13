from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import ProfileForm
from .models import Profile


@login_required(login_url='/accounts/sign_in/')
def my_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if profile:
        return render(request, 'profiles/show.html', {'profile': profile})
    messages.error(request, 'You have not setup your profile yet!')
    return HttpResponseRedirect(reverse('profile:create'))


def show_profile(request, profile_slug):
    profile = get_object_or_404(Profile, profile_uid=profile_slug)
    if request.user == profile.user:
        return HttpResponseRedirect(reverse('profile:me'))
    return render(request, 'profiles/show.html', {'profile': profile})


@login_required(login_url='/accounts/sign_in/')
def edit_profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if profile:
        form = ProfileForm(instance=profile)
        if request.method == 'POST':
            form = ProfileForm(instance=profile, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated!')
                return HttpResponseRedirect(reverse('profile:me'))
        return render(request, 'profiles/edit.html', {'form': form})

    messages.error(request, 'You have not setup your profile yet!')
    return HttpResponseRedirect(reverse('profile:create'))


@login_required(login_url='/accounts/sign_in/')
def create_profile(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, files=request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile was created!')
            return HttpResponseRedirect(reverse('profile:me'))
        messages.error(request, 'Invalid form, check fields and try again.')
    return render(request, 'profiles/create.html', {'form': form})


def show_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'profiles/list.html', {'profiles': profiles})
