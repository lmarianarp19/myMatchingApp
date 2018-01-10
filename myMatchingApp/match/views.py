from django.shortcuts import render
from django.http import HttpResponse
from .models import Community
from .forms import CommunityForm, RedForm, BlueForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.

def home(request):
    # communities = Community.objects.all()
    return render(request, 'match/base.html', {})

def community_list(request):
    communities = Community.objects.all()
    return render(request, 'match/community_list.html', {'communities': communities})

# def new_community(request):
#     if request.method == "POST":
#         form = CommunityForm(request.POST)
#         if form.is_valid():
#             community = form.save(commit=False)
#             community.save()
#             # return redirect('new_woman', id=community.id)
#             return redirect('home')
#             # return redirect('community_list')
#     else:
#         form = CommunityForm()
#     return render(request, 'match/new_community.html', {'form': form})

def new_red(request):
    if request.method == "POST":
        form = RedForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.save()
            return redirect('home')
    else:
        form = RedForm()
    return render(request, 'match/new_red.html', {'form': form})

# def new_man(request, id):
def new_blue(request):
    if request.method == "POST":
        form = BlueForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.save()
            return redirect('home')
    else:
        form = BlueForm()
    return render(request, 'match/new_blue.html', {'form': form})

class CommunityCreate(CreateView):
    model = Community
    fields = '__all__'
    # initial={'date_of_death':'05/01/2018',}

class CommunityUpdate(UpdateView):
    model = Community
    fields = ['name']

class CommunityDelete(DeleteView):
    model = Community
    success_url = reverse_lazy('community_list')


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
