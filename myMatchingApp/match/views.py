from django.shortcuts import render
from django.http import HttpResponse
from .models import Community


# Create your views here.
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'match/community_list.html', {'communities': communities})






# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
