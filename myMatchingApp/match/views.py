from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Community, Red, Blue
from .forms import CommunityForm, RedForm, BlueForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError


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
            community = form.cleaned_data['community']
            reds = Red.objects.filter(community = community)
            if reds.count() >= community.number_couples:
                raise ValidationError('There is no more space for red in this community')

            red = form.save(commit=False)
            red.save()
            return redirect('home')
    else:
        form = RedForm()
    return render(request, 'match/new_red.html', {'form': form})

def new_blue(request):
    if request.method == "POST":
        form = BlueForm(request.POST)

        # blues = Blue.objects.filter(community = community)
        # print(blues)
        if form.is_valid():
            community = form.cleaned_data['community']
            blues = Blue.objects.filter(community = community)
            # print('este es el numero de blues')
            # print(blues.count() )
            # print(isinstance(blues.count, int))

            if blues.count() >= community.number_couples:
                raise ValidationError('There is no more space for blue in this community')

            blue = form.save(commit=False)
            blue.save()
            return redirect('home')
    else:
        form = BlueForm()
    return render(request, 'match/new_blue.html', {'form': form})

# def new_man(request, id):
# def new_blue(request):
#     if request.method == "POST":
#         form = BlueForm(request.POST)
#         print('this is the reques')
#         print(request)
#         # community = Community.objects.filter(community = form.community)
#         # community = form.community
#         #reds = Red.objects.filter(community = community)
#         # blues = Blue.objects.filter(community = community)
#         # if len(blues) >= community.number_couples:
#             # raise ValidationError('There is no space for more blue members in this community')
#
#         if form.is_valid():
#             community = form.save(commit=False)
#             community.save()
#             return redirect('home')
#     else:
#         form = BlueForm()
#     return render(request, 'match/new_blue.html', {'form': form})

class CommunityCreate(CreateView):
    model = Community
    fields = '__all__'
    success_url = reverse_lazy('community_list')
    # initial={'date_of_death':'05/01/2018',}

class CommunityUpdate(UpdateView):
    model = Community
    fields = ['name']
    success_url = reverse_lazy('community_list')

class CommunityDelete(DeleteView):
    model = Community
    success_url = reverse_lazy('community_list')

def community_details(request, pk):
    community = get_object_or_404(Community, pk=pk)
    reds = Red.objects.filter(community = community)
    blues = Blue.objects.filter(community = community)
    return render(request, 'match/community_detail.html', {'community': community, 'reds': reds, 'blues': blues})

def blue_details(request, pk):
    blue = get_object_or_404(Blue, pk=pk)
    community = blue.community
    reds = Red.objects.filter(community = community)
    return render(request, 'match/blue_details.html', {'community': community, 'blue': blue, 'reds': reds})

def red_details(request, pk):
    red = get_object_or_404(Red, pk=pk)
    community = red.community
    blues = Red.objects.filter(community = community)
    return render(request, 'match/red_details.html', {'community': community, 'blues': blues, 'red': red})



# def new_blue(request):
#     blue=get_object_or_404(Blue)
#
#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#
#         # Create a form instance and populate it with data from the request (binding):
#         form = BlueForm(request.POST)
#
#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             # book_inst.due_back = form.cleaned_data['renewal_date']
#             # blue = form.save(commit=False)
#             # blue.save()
#             blue.name = form.cleaned_data['name']
#             blue.community = form.cleaned_data['community']
#             blue.save()
#
#             # redirect to a new URL:
#             # return HttpResponseRedirect(reverse('community_list') )
#             return redirect('home')
#
#     # If this is a GET (or any other method) create the default form.
#     else:
#     #     proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = BlueForm()
#
#     return render(request, 'match/new_blue.html', {'form': form})
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
