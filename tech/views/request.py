import logging

from django.shortcuts import render, redirect

from tech.forms.newrequest import NewRequestForm


def request(request):
    context = {}
    return redirect('/', msg='Thank you for submitting a request. We will review and be in touch shortly.')

    form = NewRequestForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            newrequest = form.save(commit=False)
            newrequest.customer = request.user
            newrequest.save()
            return redirect('tech:home', msg='Thank you for submitting a request. We will review and be in touch shortly.')
        else:
            return render(request, 'tech/request.html', {'form': form})
    else:
        context['form'] = form
        return render(request, 'tech/request.html', context)
