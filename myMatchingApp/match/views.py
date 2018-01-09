from django.shortcuts import render
from django.http import HttpResponse
from .models import Community
from .forms import CommunityForm, WomanForm
from django.shortcuts import redirect


# Create your views here.
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'match/community_list.html', {'communities': communities})

def new_community(request):
    if request.method == "POST":
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.save()
            return redirect('new_woman', id=community.id)
            # return redirect('community_list')
    else:
        form = CommunityForm()
    return render(request, 'match/new_community.html', {'form': form})

def new_woman(request, id):
    if request.method == "POST":
        form = WomanForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.save()
            return redirect('community_list')
    else:
        form = WomanForm()
    return render(request, 'match/new_woman.html', {'form': form})

def new_man(request, id):
    if request.method == "POST":
        form = ManForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.save()
            return redirect('community_list')
    else:
        form = ManForm()
    return render(request, 'match/new_man.html', {'form': form})


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
