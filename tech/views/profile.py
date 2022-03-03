from django.contrib.auth import login
from django.shortcuts import render, redirect

from tech.forms import RegistrationForm
from tech.forms.profile import ProfileForm


def profile(request):
    context = {}
    form = ProfileForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('tech:home')
        else:
            return render(request, 'tech/profile.html', {'form': form})
    else:
        context['form'] = form
        return render(request, 'tech/profile.html', context)