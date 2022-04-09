from django.contrib.auth import login
from django.shortcuts import render, redirect

from tech.forms import RegistrationForm


def register(request):
    context = {}
    form = RegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('tech:home')
        else:
            return render(request, 'tech/register.html', {'form': form})
    else:
        context['form'] = form
        return render(request, 'tech/register.html', context)