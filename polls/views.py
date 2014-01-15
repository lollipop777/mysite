from django.http import HttpResponse, Http404
from django.shortcuts import render

from polls.models import Poll

# Create your views here.

def index(request):
    polls = Poll.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'polls': polls})

def detail(request, poll_id):
    try:
        poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, 'polls/detail.html', {'poll': poll})

def results(request, poll_id):
    return HttpResponse('You are looking at poll %s' % poll_id)

def vote(request, poll_id):
    return HttpResponse('You are voting on poll %s' % poll_id)
