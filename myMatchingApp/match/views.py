from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Community, Red, Blue, Ranking, Matching, Pairing
from .forms import CommunityForm, RedForm, BlueForm, RankingByBlueForm, RankingByRedForm, MatchingForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.views import View


# Create your views here.

def home(request):
    # communities = Community.objects.all()
    return render(request, 'match/home.html', {})

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
            return redirect('community_details', pk = community.pk)
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
            return redirect('community_details', pk = community.pk)
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

def community_new(request):
    if request.method == "POST":
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            post.save()
            return redirect('community_list')
    else:
        form = CommunityForm()
    return render(request, 'match/community_edit.html', {'form': form})


def community_edit(request, pk):
    community = get_object_or_404(Community, pk=pk)
    if request.method == "POST":
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            community = form.save(commit=False)
            community.save()
            return redirect('community_details', pk=community.pk)
    else:
        form = CommunityForm(instance=community)
    return render(request, 'match/community_edit.html', {'form': form})

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
    add_red = can_add_members(community, reds)
    add_blue = can_add_members(community, blues)
    return render(request, 'match/community_detail.html', {'community': community, 'reds': reds, 'blues': blues, 'add_red': add_red, 'add_blue': add_blue})

def can_add_members(community, group):
    if len(group) < int(community.number_couples):
        return True
    else:
        return False

def blue_details(request, pk):
    blue = get_object_or_404(Blue, pk=pk)
    community = blue.community
    reds = Red.objects.filter(community = community)
    red_scores = []
    for red in reds:
        name_score = {}
        rank = Ranking.objects.filter(red=red, blue=blue)
        name_score['red_name'] = red.name
        name_score['red_pk'] = red.pk
        # I need this condition because sometimes the ranking is ceate with value None
        if rank and (rank[0].blue_to_red_score):
            name_score['rank_given'] = rank[0].blue_to_red_score
        else:
            name_score['rank_given'] = 'No score given yet'
        red_scores.append(name_score)
    rankings = Ranking.objects.filter(blue = blue)
    # puede ser mas de un pairing, uno por algoritmo
    pairs_algorithm = {}
    if blue.pairing:
        pairing = Pairing.objects.filter(pk = blue.pairing.pk)
        for pair in pairing:
            # no se si puedo asignar pair como nombre de un hash
            # print('this is the pair')
            # print(pair.values())
            red_algorithm = {}
            red_pair = Red.objects.filter(pairing = pair)
            red_name = red_pair[0].name
            matching = pair.matching
            # TODO cuando ponga la condicion de unique togehter matching y community puedo sacr el puntaje de red

            # happiness = Ranking.objects.filter(red = red_pair)
            # print('this is happiness')
            # print(happiness)
            # satisfaction = happiness[0].blue_to_red_score
            # tal ves esto no funciona porque talvez matching es solo una id y no todo el modelo
            algorithm = matching.algorithm
            red_algorithm['red_name'] = red_name
            red_algorithm['algorithm'] = algorithm
            # red_algorithm['happiness'] = satisfaccion
            pairs_algorithm[pair.pk] = red_algorithm
        print('this is the pairs_algorithm')
        esto = pairs_algorithm
        print(esto)
    return render(request, 'match/blue_details.html', {'blue': blue,  'blue_id': pk, 'red_scores' : red_scores,  'pairs_algorithm': pairs_algorithm, 'community': community })


def red_details(request, pk):
    red = get_object_or_404(Red, pk=pk)
    community = red.community
    # get the blues that belong to this community
    blues = Blue.objects.filter(community = community)
    blue_scores = []
    for blue in blues:
        # hash to store the name of the blue and the score given by red.
        name_score = {}
        # get the ranking that have red and blue
        rank = Ranking.objects.filter(red=red, blue=blue)
        name_score['blue_name'] = blue.name
        name_score['blue_pk'] = blue.pk
        if rank and (rank[0].red_to_blue_score):
            name_score['rank_given'] = rank[0].red_to_blue_score
        else:
            name_score['rank_given'] = 'No score given yet'
        blue_scores.append(name_score)


    rankings = Ranking.objects.filter(red = red)

    # in case there is  a pair, it gives the pair and the algoritm.
    pairs_algorithm = {}
    if red.pairing:
        pairing = Pairing.objects.filter(pk = red.pairing.pk)
        for pair in pairing:
            blue_algorithm = {}
            blue_pair = Blue.objects.filter(pairing = pair)
            blue_name = blue_pair[0].name
            matching = pair.matching
            algorithm = matching.algorithm
            blue_algorithm['blue_name'] = blue_name
            blue_algorithm['algorithm'] = algorithm
            pairs_algorithm[pair.pk] = blue_algorithm
    return render(request, 'match/red_details.html', {'red': red,  'red_id': pk, 'blue_scores' : blue_scores,  'pairs_algorithm': pairs_algorithm, 'community' : community })

def new_ranking_by_blue(request, red_id, blue_id):
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
            form =  RankingByBlueForm(request.POST, instance = ranking.first())
        else:
            # if ranking doesn't exist create a new instance of ranking.
            form = RankingByBlueForm(request.POST)
        if form.is_valid():
            ranking = form.save(commit=False)
            # add blue and red to the ranking model
            ranking.blue = blue
            ranking.red = red
            ranking.save()
            return redirect('blue_details', pk = blue.pk)
    else:
        form = RankingByBlueForm()
    return render(request, 'match/new_ranking_by_blue.html', {'form': form, 'red': red})

def new_ranking_by_red(request, blue_id, red_id):
    # TODO ver si puedo limpiar esto, haciendo solo una funcion para azul y rojo
    blue_id = int(blue_id)
    red_id = int(red_id)
    blue = Blue.objects.get(pk = blue_id)
    red = Red.objects.get(pk = red_id)
    ranking = Ranking.objects.filter(red = red, blue = blue)
    if request.method == "POST":
        if ranking:
            # the red and blue form are different because in the red form I want to rank blue and viceversa
            form =  RankingByRedForm(request.POST, instance = ranking.first())
        else:
            form = RankingByRedForm(request.POST)
        if form.is_valid():
            ranking = form.save(commit=False)
            ranking.blue = blue
            ranking.red = red
            ranking.save()
            return redirect('red_details',  pk = red_id)
    else:
        form = RankingByRedForm()
    return render(request, 'match/new_ranking_by_red.html', {'form': form, 'blue':blue})

def ranking_list(request):
    rankings = Ranking.objects.all()
    return render(request, 'match/ranking_list.html', {'rankings': rankings})


class New_matching(View):
    form_class = MatchingForm
    # Que hace este initial??
    initial = {'key': 'value'}
    template = 'match/new_matching.html'
    def __init__(self):
        self.tentative_engagements = []
        self.free_proposer = []
        self.proposer_ranking = {}
        self.recipient_ranking = {}

    def get(self, request):
        # Por que necesito el get???
        form = self.form_class(initial=self.initial)
        return render(request, self.template, {'form': form})

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
            if (algorithm == 'Shapley Gale Blue Proposes'):
                self.proposer_ranking = ranks_blue_to_red
                self.recipient_ranking = ranks_red_to_blue
                proposer_instance = blues
                recipent_instance = reds
                proposer = Blue
                recipient = Red
            elif(algorithm == 'Shapley Gale Red Proposes'):
                self.proposer_ranking = ranks_red_to_blue
                self.recipient_ranking = ranks_blue_to_red
                proposer_instance = reds
                recipient_instance = blues
                proposer = Red
                recipient = Blue
            self.all_proposer(proposer_instance)
            print('this is all proposer')
            print(self.all_proposer)
            # self.free_proposer =all_proposer(self, proposer_instance)
            self.another_iteration_step()
            print('this is the final match')
            print(self.tentative_engagements)
            matching = form.save(commit = False)
            matching.save()
            for subarray in self.tentative_engagements:
                self.make_pair(proposer, recipient, subarray, community, matching)
            # pairing_new = Pairing(matching = matching)
            # pairing_new.save()


            return redirect('matching_details', pk = matching.pk)

        # else:
        #     form = MatchingForm()
        return render(request, self.template, {'form': form})

    def make_pair(self, proposer, recipient, subarray, community, matching):
        get_proposer = proposer.objects.filter(name = subarray[0], community = community)[0]
        get_recipient = recipient.objects.filter(name = subarray[1], community = community)[0]
        pairing_new = Pairing(matching = matching)
        pairing_new.save()
        get_proposer.pairing = pairing_new
        get_recipient.pairing = pairing_new
        get_proposer.save()
        get_recipient.save()




    def all_proposer(self, proposer):
        # este metodo lo puedo poner afuera, como en las ultima lineas o lo puedo poner dentro de la clase, que es mejor?
        # get the proposer names
        for person in proposer:
            self.free_proposer.append(person.name)

        # return self.free_proposer

    def another_iteration_step(self):
        # maybe I will have problems with tantative_engagements
        print('indide another_iteration_step')
        #run the algorithm until there is no single proposer.
        while(len(self.free_proposer) > 0):
            for person in self.free_proposer:
                self.begin_matching(person)

    def begin_matching(self, actual_proposer):
        print('dealing with %s'%(actual_proposer))

        option = 1
        single = True

        # quiero regresar a la for loop si la persona no se le ha propuesto a nadie
        while single:
            # continue iteraiting until the person is match
            for recipient, rank in self.proposer_ranking[actual_proposer].items():
                print('we are looking for the option %s'%(option))
                # if the element at the dictionary is the option that I'm looking for, i start looking for the first option
                # if the fist option is no available for me i go to the second option ...
                if(int(rank) == option ):
                    # n = n + 1
                    # array of arrays with the engagement for this option.
                    # EX: [['carlos', 'ana']]
                    already_match = [ couple for couple in self.tentative_engagements if recipient in couple]
                    print('this is already_match %s'%(already_match))
                    if(len(already_match) == 0 ):
                        print('the option num %s'%(option))
                        print('is avaliable for %s'%(actual_proposer))
                        self.tentative_engagements.append([actual_proposer, recipient])
                        self.free_proposer.remove(actual_proposer)
                        # I want to break the full for loop.
                        single = False
                        print (self.tentative_engagements)
                        break
                    elif(len(already_match) > 0):
                        print('this is already_match')
                        print(already_match)
                        print('this is recipient_ranking')
                        print(self.recipient_ranking)
                        # get the score that the recipikent gives for the current_match
                        current_match = self.recipient_ranking[recipient][already_match[0][0]]
                        # get the score that the recipient gives to the actual_proposer
                        this_match = self.recipient_ranking[recipient][actual_proposer]
                        #  if she prefers the current_match the actual proposer goes with the next option.
                        if(current_match < this_match):
                            print('she is satisifed with %s..'%(already_match[0][0]))
                            option = option + 1
                            print (self.tentative_engagements)
                            break
                        else:
                        # if she prefers the actual proposer they get engaged
                            print('she prefers the man that we are evaluationg')
                            # remove the last engagement
                            self.free_proposer.remove(actual_proposer)
                            # the guy becomes single now
                            self.free_proposer.append(already_match[0][0])
                            print('here we change the tentative match')
                            print('tentative_engagements before %s'%(self.tentative_engagements))
                            # she gets engaged with the actual_proposer
                            already_match[0][0] = actual_proposer
                            print('tentative_engagements after the change %s'%(self.tentative_engagements))
                            single = False
                            # print (self.tentative_engagements)
                            break
def matching_list(request):
    matching = Matching.objects.all()
    return render(request, 'match/matching_list.html', {'matching': matching})




def pairing_list(request):
    pairing = Pairing.objects.all()
    print('this are the pairing')
    print(pairing)
    return render(request, 'match/pairing_list.html', {'pairing': pairing})

def matching_details(request, pk):
    matching = get_object_or_404(Matching, pk=pk)
    community = matching.community
    # algorithm = matching.algorithm
    pairs = Pairing.objects.filter(matching = matching)
    pairs_array = []
    for pair in pairs:
        couple = []
        # red = Red.objects.filter(pairing = pair)[0].name
        # blue = Blue.objects.filter(pairing = pair)[0].name
        red = Red.objects.filter(pairing = pair)[0]
        blue = Blue.objects.filter(pairing = pair)[0]
        # talvez tengo que quitar el [0],name de red y blue y ponerlo cuando append a couple
        ranking = Ranking.objects.filter(red = red, blue = blue)
        blue_happiness = ranking[0].blue_to_red_score
        red_happiness = ranking[0].red_to_blue_score
        couple.append(blue.name)
        couple.append(red.name)
        couple.append(blue_happiness)
        couple.append(red_happiness)
        pairs_array.append(couple)
    return render(request, 'match/matching_details.html', {'matching': matching, 'pairs': pairs, 'pairs_array' : pairs_array, 'community' : community })

class MatchingDelete(DeleteView):
    model = Matching
    success_url = reverse_lazy('matching_list')




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

# def all_proposer(proposer):
#
#     # get the proposer names
#     free_proposer = []
#     for person in proposer:
#         free_proposer.append(person.name)
#     return free_proposer
