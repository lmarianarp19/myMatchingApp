from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Community, Red, Blue, Ranking, Matching
from .forms import CommunityForm, RedForm, BlueForm, RankingBlueForm, RankingRedForm, MatchingForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.views import View


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
            if blues.count() >= community.number_couples:
                raise ValidationError('There is no more space for blue in this community')

            blue = form.save(commit=False)
            blue.save()
            return redirect('home')
    else:
        form = BlueForm()
    return render(request, 'match/new_blue.html', {'form': form})

def ranking_list(request):
    rankings = Ranking.objects.all()
    return render(request, 'match/ranking_list.html', {'rankings': rankings})

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
    return render(request, 'match/blue_details.html', {'community': community, 'blue': blue, 'reds': reds, 'blue_id': pk})

def red_details(request, pk):
    red = get_object_or_404(Red, pk=pk)
    community = red.community
    # TODO sera qut tengo que cmabiar esto? es blues con red
    blues = Blue.objects.filter(community = community)
    return render(request, 'match/red_details.html', {'community': community, 'blues': blues, 'red': red, 'red_id': pk})

def new_ranking_blue(request, red_id, blue_id):
    # the id are strings, I need to pass it to integers
    blue_id = int(blue_id)
    red_id = int(red_id)
    #get the blu and red objects with that id
    blue = Blue.objects.get(pk = blue_id)
    red = Red.objects.get(pk = red_id)
    #check if this ranking already exist
    ranking = Ranking.objects.filter(blue = blue, red = red)

    if request.method == "POST":
        # if the ranking exists
        if ranking:
            # edit the actual ranking instance.
            form =  RankingBlueForm(request.POST, instance = ranking.first())
        else:
            # if ranking doesn't exist create a new instance of ranking.
            form = RankingBlueForm(request.POST)
        if form.is_valid():
            ranking = form.save(commit=False)
            # add blue and red to the ranking model
            ranking.blue = blue
            ranking.red = red
            ranking.save()
            return redirect('home')
    else:
        form = RankingBlueForm()
    return render(request, 'match/new_ranking_blue.html', {'form': form})

def new_ranking_red(request, blue_id, red_id):
    # TODO ver si puedo limpiar esto, haciendo solo una funcion para azul y rojo
    blue_id = int(blue_id)
    red_id = int(red_id)
    blue = Blue.objects.get(pk = blue_id)
    red = Red.objects.get(pk = red_id)
    ranking = Ranking.objects.filter(red = red, blue = blue)
    if request.method == "POST":
        if ranking:
            # the red and blue form are different because in the red form I want to rank blue and viceversa
            form =  RankingRedForm(request.POST, instance = ranking.first())
        else:
            form = RankingRedForm(request.POST)
        if form.is_valid():
            ranking = form.save(commit=False)
            ranking.blue = blue
            ranking.red = red
            ranking.save()
            return redirect('home')
    else:
        form = RankingRedForm()
    return render(request, 'match/new_ranking_red.html', {'form': form})

def ranking_list(request):
    rankings = Ranking.objects.all()
    return render(request, 'match/ranking_list.html', {'rankings': rankings})


class New_matching(View):
    tentative_engagements = []
    free_proposer = []
    proposer_ranking = {}
    recipient_ranking = {}
    form_class = MatchingForm
    # en el ejemplo en linea tienen un campo con un hash y la template en esta parte

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            community = form.cleaned_data['community']
            algorithm = form.cleaned_data['algorithm']
            # encontrar los azules y rojos
            blues = Blue.objects.filter(community = community)
            reds = Red.objects.filter(community = community)
            # hash to store all the rankings from blue to red
            ranks_blue_to_red = {}
            ranks_red_to_blue = {}
            for blue in blues:
                # hash to store the ranking to the red make by this blue
                blue_to_red = {}
                # get all the rankings that have this blue
                blue_ranking  = Ranking.objects.filter(blue = blue)
                for rank in blue_ranking:
                    # store the ranking froms this blue to each red
                    # intentando poner .name
                    blue_to_red[rank.red.name] = rank.blue_to_red_score
                ranks_blue_to_red[blue.name] = blue_to_red

            for red in reds:
                # hash to store the ranking to the red make by this blue
                red_to_blue = {}
                # get all the rankings that have this blue
                red_ranking  = Ranking.objects.filter(red = red)
                for rank in red_ranking:
                    # store the ranking froms this blue to each red
                    red_to_blue[rank.blue.name] = rank.red_to_blue_score
                ranks_red_to_blue[rank.red.name] = red_to_blue

            # set who is the proposer and who is the recipent
            if (algorithm == 'SGBP'):
                self.proposer_ranking = ranks_blue_to_red
                self.recipient_ranking = ranks_red_to_blue
                proposer_instance = blues
                recipent_instance = reds
            elif(algorithm == 'SGRP'):
                self.proposer_ranking = ranks_red_to_blue
                self.recipient_ranking = ranks_blue_to_red
                proposer_instance = blues
                recipient_instance = red

            self.free_proposer = all_proposer(proposer_instance)
            self.another_iteration_step()
            return redirect('home')

        else:
            form = MatchingForm()
        return render(request, 'match/new_matching.html', {'form': form})

    def all_proposer(proposer):
        # get the proposer names
        for person in proposer:
            self.free_proposer.append(person.name)

        return self.free_proposer

    def another_iteration_step():
        # maybe I will have problems with tantative_engagements
        print('indide another_iteration_step')
        #run the algorithm until there is no single proposer.
        while(len(self.free_proposer) > 0):
            for person in self.free_proposer:
                self.begin_matching(person)

    def begin_matching(actual_proposer):
        print('dealing with %s'%(actual_proposer))

        option = 1
        single = True

        # quiero regresar a la for loop si la persona no se le ha propuesto a nadie
        while single:
            # continue iteraiting until the person is match
            for recipient, rank in self.proposer_ranking[actual_proposer].items():
                print('we are looking for the option %s'%(option))
                if(int(rank) == option ):
                    # n = n + 1
                    already_match = [ couple for couple in self.tentative_engagements if recipient in couple]
                    print('this is already_match %s'%(already_match))
                    if(len(already_match) == 0 ):
                        print('the option num %s'%(option-1))
                        print('is avaliable for %s'%(actual_proposer))
                        self.tentative_engagements.append([actual_proposer, recipient])
                        self.free_proposer.remove(actual_proposer)
                        # I want to break the full for loop.
                        single = False
                        print (self.tentative_engagements)
                        break
                    elif(len(already_match) > 0):
                            current_match = self.recipient_ranking[recipient][already_match[0][0]]
                            this_match = self.recipient_ranking[recipient][actual_proposer]
                            if(current_match < this_match):
                                print('she is satisifed with %s..'%(already_match[0][0]))
                                option = option + 1
                                print (self.tentative_engagements)
                                break
                            else:
                                print('she prefers the man that we are evaluationg')
                                self.free_proposer.remove(actual_proposer)
                                self.free_proposer.append(already_match[0][0])
                                print('here we change the tentative match')
                                print('tentative_engagements before %s'%(tentative_engagements))
                                already_match[0][0] = actual_proposer
                                print('tentative_engagements after the change %s'%(tentative_engagements))
                                single = False
                                print (self.tentative_engagements)
                                break




#
# def new_matching(request):
#     if request.method == "POST":
#         form = MatchingForm(request.POST)
#         if form.is_valid():
#             community = form.cleaned_data['community']
#             algorithm = form.cleaned_data['algorithm']
#             # encontrar los azules y rojos
#             blues = Blue.objects.filter(community = community)
#             reds = Red.objects.filter(community = community)
#             # hash to store all the rankings from blue to red
#             ranks_blue_to_red = {}
#             ranks_red_to_blue = {}
#             for blue in blues:
#                 # hash to store the ranking to the red make by this blue
#                 blue_to_red = {}
#                 # get all the rankings that have this blue
#                 blue_ranking  = Ranking.objects.filter(blue = blue)
#                 for rank in blue_ranking:
#                     # store the ranking froms this blue to each red
#                     # intentando poner .name
#                     blue_to_red[rank.red.name] = rank.blue_to_red_score
#                 ranks_blue_to_red[blue.name] = blue_to_red
#
#             for red in reds:
#                 # hash to store the ranking to the red make by this blue
#                 red_to_blue = {}
#                 # get all the rankings that have this blue
#                 red_ranking  = Ranking.objects.filter(red = red)
#                 for rank in red_ranking:
#                     # store the ranking froms this blue to each red
#                     red_to_blue[rank.blue.name] = rank.red_to_blue_score
#                 ranks_red_to_blue[rank.red.name] = red_to_blue
#
#             # set who is the proposer and who is the recipent
#             if (algorithm == 'SGBP'):
#                 proposer_ranking = ranks_blue_to_red
#                 recipient_ranking = ranks_red_to_blue
#                 proposer_instance = blues
#                 recipent_instance = reds
#             elif(algorithm == 'SGRP'):
#                 proposer_ranking = ranks_red_to_blue
#                 recipient_ranking = ranks_blue_to_red
#                 proposer_instance = blues
#                 recipient_instance = red
#             free_proposer = all_proposer(proposer_instance)
#             # print('this are the proposer names')
#             # print(free_proposer)
#             tentative_engagements = []
#             another_iteration_step(free_proposer, proposer_ranking, tentative_engagements)
#             return redirect('home')
#
#     else:
#         form = MatchingForm()
#     return render(request, 'match/new_matching.html', {'form': form})



# def all_proposer(proposer):
#     # get the proposer names
#     proposer_names = []
#     for person in proposer:
#         proposer_names.append(person.name)
#
#     return proposer_names

# def another_iteration_step(proposer_names, proposer_ranking, tentative_engagements):
#     # maybe I will have problems with tantative_engagements
#     print('indide another_iteration_step')
#     #run the algorithm until there is no single proposer.
#     while(len(proposer_names) > 0):
#         for person in proposer_names:
#             begin_matching(person, proposer_ranking, tentative_engagements, proposer_names)

# def begin_matching(actual_proposer, proposer_ranking, tentative_engagements, proposer_names):
#     print('dealing with %s'%(actual_proposer))
#
#     option = 1
#     single = True
#
#     # quiero regresar a la for loop si la persona no se le ha propuesto a nadie
#     while single:
#         # continue iteraiting until the person is match
#         for recipient, rank in proposer_ranking[actual_proposer].items():
#             print('we are looking for the option %s'%(option))
#             if(int(rank) == option ):
#                 # n = n + 1
#                 already_match = [ couple for couple in tentative_engagements if recipient in couple]
#                 print('this is already_match %s'%(already_match))
#                 if(len(already_match) == 0 ):
#                     print('the option num %s'%(option-1))
#                     print('is avaliable for %s'%(actual_proposer))
#                     tentative_engagements.append([actual_proposer, recipient])
#                     proposer_names.remove(actual_proposer)
#                     # I want to break the full for loop.
#                     single = False
#                     print (tentative_engagements)
#                     break
#                 elif(len(already_match) > 0):
#                         current_match = recipient_ranking[recipient][already_match[0][0]]
#                         this_match = recipient_ranking[recipient][actual_proposer]
#                         if(current_match < this_match):
#                             print('she is satisifed with %s..'%(already_match[0][0]))
#                             option = option + 1
#                             print (tentative_engagements)
#                             break
#                         else:
#                             print('she prefers the man that we are evaluationg')
#                             free_proposer.remove(actual_proposer)
#                             free_proposer.append(already_match[0][0])
#                             print('here we change the tentative match')
#                             print('tentative_engagements before %s'%(tentative_engagements))
#                             already_match[0][0] = actual_proposer
#                             print('tentative_engagements after the change %s'%(tentative_engagements))
#                             single = False
#                             print (tentative_engagements)
#                             break
#     return tentative_engagements, proposer_names



            # print ('this are the rankings '

            # reds = Red.objects.filter(community = community)
            # if reds.count() >= community.number_couples:
            #     raise ValidationError('There is no more space for red in this community')
            #
            # red = form.save(commit=False)
            # red.save()
            # return redirect('home')

# funcion que mira asigna quien es el que propone.
# def set_proposer_recipient(proposer):
#     # global proposer_ranking
#     # global recipient_ranking
#     # set who is the proposer and who is the recipient
#     if (proposer == 'SGBP'):
#         proposer_ranking = men_ranking
#         recipient_ranking = women_ranking
#     elif(proposer == 'SGRP'):
#         proposer_ranking = women_ranking
#         recipient_ranking = men_ranking
#     return proposer_ranking, recipient_ranking



# class MatchingCreate(CreateView):
#     model = Matching
#     fields = '__all__'
#     success_url = reverse_lazy('home')
#     # initial={'date_of_death':'05/01/2018',}
#
# class MatchingUpdate(UpdateView):
#     model = Matching
#     fields = '__all__'
#     success_url = reverse_lazy('home')
#
# class MatchingDelete(DeleteView):
#     model = Matching
#     success_url = reverse_lazy('home')
        # community = Community.objects.filter(community = form.community)
        # community = form.community
        #reds = Red.objects.filter(community = community)
        # blues = Blue.objects.filter(community = community)
        # if len(blues) >= community.number_couples:
            # raise ValidationError('There is no space for more blue members in this community')

    #     if form.is_valid():
    #         ranking = form.save(commit=False)
    #         ranking.save()
    #         return redirect('home')
    # else:
    #     form = RankingForm()
    # return render(request, 'match/new_ranking.html', {'form': form})
















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
